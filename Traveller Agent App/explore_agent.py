import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from base_agent import BaseAgent
from models import (
    TravelRequest, Destination, Attraction, Restaurant, TravelMood, 
    AgentResponse
)
from mock_data import MockDataGenerator

class ExploreAgent(BaseAgent):
    """Agent specialized in suggesting attractions, restaurants, and activities"""
    
    def __init__(self):
        super().__init__(
            name="ExploreAgent",
            description="Specialized in discovering and recommending the best attractions, restaurants, and activities at travel destinations."
        )
        
        # Add exploration-specific tools
        self.add_tool({
            "name": "find_attractions",
            "description": "Find tourist attractions and points of interest",
            "parameters": {
                "destination": "Destination city",
                "interests": "User interests and preferences",
                "budget": "Budget level",
                "duration": "Trip duration"
            }
        })
        
        self.add_tool({
            "name": "recommend_restaurants",
            "description": "Find restaurants and dining options",
            "parameters": {
                "destination": "Destination city",
                "cuisine_preferences": "Preferred cuisines",
                "budget": "Budget level",
                "dietary_restrictions": "Any dietary restrictions"
            }
        })
        
        self.add_tool({
            "name": "plan_itinerary",
            "description": "Create a day-by-day itinerary",
            "parameters": {
                "destination": "Destination city",
                "attractions": "Selected attractions",
                "restaurants": "Selected restaurants",
                "duration": "Trip duration",
                "preferences": "User preferences"
            }
        })
    
    async def process_request(self, request: Dict[str, Any]) -> AgentResponse:
        """Process an exploration request"""
        try:
            destination = request.get("destination")
            travel_request = request.get("travel_request")
            user_preferences = request.get("preferences", {})
            
            if not destination or not travel_request:
                return self.create_response(
                    success=False,
                    message="Missing required information: destination and travel_request",
                    data=None
                )
            
            self.add_to_history("user", f"Exploration request for {destination.name} with {travel_request.mood.value} mood")
            
            # Generate exploration recommendations using Gemini
            exploration_prompt = f"""
            Help me create an amazing exploration plan for this destination:
            
            Destination: {destination.name}, {destination.country}
            Travel Mood: {travel_request.mood.value}
            Budget: {travel_request.budget.value}
            Trip Duration: {self._calculate_duration(travel_request)} days
            Special Requirements: {travel_request.special_requirements}
            
            Please provide recommendations for:
            1. Must-visit attractions that match the travel mood
            2. Best restaurants and local cuisine experiences
            3. Hidden gems and off-the-beaten-path locations
            4. Day-by-day itinerary suggestions
            5. Local tips and cultural insights
            
            Focus on creating an authentic, memorable experience that matches the user's preferences.
            """
            
            gemini_response = await self.call_gemini(exploration_prompt)
            self.add_to_history("assistant", gemini_response)
            
            # Generate attractions
            attractions = await self._get_attractions(destination, travel_request)
            
            # Generate restaurants
            restaurants = await self._get_restaurants(destination, travel_request)
            
            # Create itinerary
            itinerary = await self._create_itinerary(destination, attractions, restaurants, travel_request)
            
            # Create exploration summary
            exploration_summary = {
                "destination": destination,
                "attractions": attractions,
                "restaurants": restaurants,
                "itinerary": itinerary,
                "exploration_recommendations": gemini_response,
                "local_tips": self._generate_local_tips(destination, travel_request)
            }
            
            response_message = f"""
            I've discovered amazing things to explore in {destination.name}:
            
            ATTRACTIONS ({len(attractions)} recommendations):
            {self._format_attractions(attractions)}
            
            RESTAURANTS ({len(restaurants)} recommendations):
            {self._format_restaurants(restaurants)}
            
            ITINERARY:
            {self._format_itinerary(itinerary)}
            
            {gemini_response}
            """
            
            return self.create_response(
                success=True,
                message=response_message,
                data=exploration_summary
            )
            
        except Exception as e:
            return self.create_response(
                success=False,
                message=f"Error processing exploration request: {str(e)}",
                data=None
            )
    
    async def _get_attractions(self, destination: Destination, travel_request: TravelRequest) -> List[Attraction]:
        """Get attraction recommendations"""
        # Generate mock attractions based on destination and mood
        attractions = MockDataGenerator.generate_attractions(
            destination=destination.name,
            mood=travel_request.mood,
            num_options=8
        )
        
        # Sort by rating and relevance
        attractions.sort(key=lambda x: x.rating, reverse=True)
        
        return attractions[:6]  # Return top 6 attractions
    
    async def _get_restaurants(self, destination: Destination, travel_request: TravelRequest) -> List[Restaurant]:
        """Get restaurant recommendations"""
        # Generate mock restaurants
        restaurants = MockDataGenerator.generate_restaurants(
            destination=destination.name,
            num_options=8
        )
        
        # Sort by rating
        restaurants.sort(key=lambda x: x.rating, reverse=True)
        
        return restaurants[:6]  # Return top 6 restaurants
    
    async def _create_itinerary(self, destination: Destination, attractions: List[Attraction], 
                               restaurants: List[Restaurant], travel_request: TravelRequest) -> List[Dict]:
        """Create a day-by-day itinerary"""
        trip_duration = self._calculate_duration(travel_request)
        itinerary = []
        
        # Distribute attractions and restaurants across days
        attractions_per_day = max(1, len(attractions) // trip_duration)
        restaurants_per_day = max(1, len(restaurants) // trip_duration)
        
        for day in range(1, trip_duration + 1):
            day_attractions = attractions[(day-1)*attractions_per_day:day*attractions_per_day]
            day_restaurants = restaurants[(day-1)*restaurants_per_day:day*restaurants_per_day]
            
            # Fill remaining slots if needed
            if len(day_attractions) < attractions_per_day and len(attractions) > day*attractions_per_day:
                day_attractions.extend(attractions[day*attractions_per_day:day*attractions_per_day + 1])
            
            if len(day_restaurants) < restaurants_per_day and len(restaurants) > day*restaurants_per_day:
                day_restaurants.extend(restaurants[day*restaurants_per_day:day*restaurants_per_day + 1])
            
            day_plan = {
                "day": day,
                "morning": {
                    "activity": day_attractions[0] if day_attractions else None,
                    "restaurant": day_restaurants[0] if day_restaurants else None
                },
                "afternoon": {
                    "activity": day_attractions[1] if len(day_attractions) > 1 else None,
                    "restaurant": day_restaurants[1] if len(day_restaurants) > 1 else None
                },
                "evening": {
                    "activity": day_attractions[2] if len(day_attractions) > 2 else None,
                    "restaurant": day_restaurants[2] if len(day_restaurants) > 2 else None
                },
                "tips": self._generate_day_tips(day, destination, travel_request)
            }
            
            itinerary.append(day_plan)
        
        return itinerary
    
    def _calculate_duration(self, travel_request: TravelRequest) -> int:
        """Calculate trip duration in days"""
        if travel_request.start_date and travel_request.end_date:
            return (travel_request.end_date - travel_request.start_date).days
        return 7  # Default 7 days
    
    def _generate_local_tips(self, destination: Destination, travel_request: TravelRequest) -> List[str]:
        """Generate local tips for the destination"""
        tips = [
            f"Best time to visit {destination.name} is {destination.best_time_to_visit}",
            f"Average temperature in {destination.name}: {destination.average_temperature}",
            "Learn a few basic phrases in the local language",
            "Carry cash for small purchases and tips",
            "Download offline maps before your trip",
            "Check local customs and dress codes",
            "Book popular attractions in advance",
            "Try local transportation options"
        ]
        
        # Add mood-specific tips
        if travel_request.mood == TravelMood.ADVENTURE:
            tips.extend([
                "Pack comfortable hiking shoes",
                "Check weather conditions before outdoor activities",
                "Consider hiring a local guide for adventure activities"
            ])
        elif travel_request.mood == TravelMood.CULTURE:
            tips.extend([
                "Research local customs and traditions",
                "Visit museums during off-peak hours",
                "Attend local cultural events if available"
            ])
        elif travel_request.mood == TravelMood.FOOD:
            tips.extend([
                "Try street food for authentic local flavors",
                "Ask locals for restaurant recommendations",
                "Consider taking a cooking class"
            ])
        
        return tips[:8]  # Return top 8 tips
    
    def _generate_day_tips(self, day: int, destination: Destination, travel_request: TravelRequest) -> List[str]:
        """Generate tips for a specific day"""
        tips = [
            "Start your day early to avoid crowds",
            "Wear comfortable walking shoes",
            "Carry water and snacks",
            "Don't forget your camera"
        ]
        
        if day == 1:
            tips.extend([
                "Take time to adjust to the local time zone",
                "Visit a nearby landmark to get oriented",
                "Try a local coffee shop to start your day"
            ])
        elif day == self._calculate_duration(travel_request):
            tips.extend([
                "Save some energy for your last day",
                "Visit any must-see places you missed",
                "Consider a relaxing evening activity"
            ])
        
        return tips
    
    def _format_attractions(self, attractions: List[Attraction]) -> str:
        """Format attractions for display"""
        formatted = ""
        for i, attraction in enumerate(attractions, 1):
            formatted += f"""
{i}. {attraction.name} ({attraction.category})
   Rating: {attraction.rating}★ | {attraction.price_range}
   Location: {attraction.location}
   Hours: {attraction.opening_hours}
   Best Time: {attraction.best_time_to_visit}
   Description: {attraction.description}
"""
        return formatted
    
    def _format_restaurants(self, restaurants: List[Restaurant]) -> str:
        """Format restaurants for display"""
        formatted = ""
        for i, restaurant in enumerate(restaurants, 1):
            formatted += f"""
{i}. {restaurant.name} ({restaurant.cuisine})
   Rating: {restaurant.rating}★ | {restaurant.price_range}
   Location: {restaurant.location}
   Hours: {restaurant.opening_hours}
   Specialties: {', '.join(restaurant.specialties[:3])}
   {f'Reservation Required' if restaurant.reservation_required else 'Walk-ins Welcome'}
"""
        return formatted
    
    def _format_itinerary(self, itinerary: List[Dict]) -> str:
        """Format itinerary for display"""
        formatted = ""
        for day_plan in itinerary:
            formatted += f"""
DAY {day_plan['day']}:
   Morning: {day_plan['morning']['activity'].name if day_plan['morning']['activity'] else 'Free time'}
   Lunch: {day_plan['morning']['restaurant'].name if day_plan['morning']['restaurant'] else 'Local choice'}
   Afternoon: {day_plan['afternoon']['activity'].name if day_plan['afternoon']['activity'] else 'Free time'}
   Dinner: {day_plan['afternoon']['restaurant'].name if day_plan['afternoon']['restaurant'] else 'Local choice'}
   Evening: {day_plan['evening']['activity'].name if day_plan['evening']['activity'] else 'Relax'}
   Tips: {', '.join(day_plan['tips'][:2])}
"""
        return formatted
    
    async def get_attraction_details(self, attraction_id: str) -> AgentResponse:
        """Get detailed information about a specific attraction"""
        # This would typically query a database
        # For now, return mock data
        return self.create_response(
            success=True,
            message="Attraction details retrieved",
            data={
                "attraction_id": attraction_id,
                "details": "Detailed information about the attraction",
                "reviews": "Recent visitor reviews",
                "photos": "Photo gallery",
                "location": "Exact location and directions"
            }
        )
    
    async def get_restaurant_details(self, restaurant_id: str) -> AgentResponse:
        """Get detailed information about a specific restaurant"""
        # This would typically query a database
        # For now, return mock data
        return self.create_response(
            success=True,
            message="Restaurant details retrieved",
            data={
                "restaurant_id": restaurant_id,
                "details": "Detailed information about the restaurant",
                "menu": "Sample menu items",
                "reviews": "Recent diner reviews",
                "reservation": "Reservation information"
            }
        ) 