import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta

from base_agent import BaseAgent
from models import (
    TravelRequest, Flight, Hotel, Destination, BudgetLevel, 
    AgentResponse, TravelPlan
)
from mock_data import MockDataGenerator

class BookingAgent(BaseAgent):
    """Agent specialized in booking flights and hotels"""
    
    def __init__(self):
        super().__init__(
            name="BookingAgent",
            description="Specialized in finding and booking the best flights and hotels based on user preferences and budget."
        )
        
        # Add booking-specific tools
        self.add_tool({
            "name": "get_flights",
            "description": "Search for available flights between two locations",
            "parameters": {
                "origin": "Departure city",
                "destination": "Arrival city", 
                "date": "Travel date",
                "passengers": "Number of passengers",
                "preferences": "Flight preferences (direct, budget, etc.)"
            }
        })
        
        self.add_tool({
            "name": "suggest_hotels",
            "description": "Find hotels at the destination",
            "parameters": {
                "destination": "Destination city",
                "check_in": "Check-in date",
                "check_out": "Check-out date",
                "guests": "Number of guests",
                "budget": "Budget level",
                "preferences": "Hotel preferences (amenities, location, etc.)"
            }
        })
        
        self.add_tool({
            "name": "book_travel",
            "description": "Complete the booking process for flights and hotels",
            "parameters": {
                "flight_id": "Selected flight ID",
                "hotel_id": "Selected hotel ID",
                "passenger_info": "Passenger details",
                "payment_info": "Payment information"
            }
        })
    
    async def process_request(self, request: Dict[str, Any]) -> AgentResponse:
        """Process a booking request"""
        try:
            travel_request = request.get("travel_request")
            selected_destination = request.get("destination")
            user_preferences = request.get("preferences", {})
            
            if not travel_request or not selected_destination:
                return self.create_response(
                    success=False,
                    message="Missing required information: travel_request and destination",
                    data=None
                )
            
            self.add_to_history("user", f"Booking request for {selected_destination.name} with {travel_request.budget.value} budget")
            
            # Generate booking recommendations using Gemini
            booking_prompt = f"""
            Help me create a comprehensive booking plan for this travel request:
            
            Destination: {selected_destination.name}, {selected_destination.country}
            Travel Dates: {travel_request.start_date} to {travel_request.end_date}
            Budget: {travel_request.budget.value}
            Travelers: {travel_request.num_travelers}
            Special Requirements: {travel_request.special_requirements}
            
            Please provide recommendations for:
            1. Best flight options (considering price, duration, and convenience)
            2. Hotel recommendations (matching budget and preferences)
            3. Any booking tips or considerations
            
            Focus on providing practical, cost-effective options that match the user's budget and preferences.
            """
            
            gemini_response = await self.call_gemini(booking_prompt)
            self.add_to_history("assistant", gemini_response)
            
            # Generate flight options
            flights = await self._get_flight_options(travel_request, selected_destination)
            
            # Generate hotel options
            hotels = await self._get_hotel_options(travel_request, selected_destination)
            
            # Calculate total costs
            total_cost = self._calculate_total_cost(flights, hotels, travel_request)
            
            # Create booking summary
            booking_summary = {
                "destination": selected_destination,
                "flights": flights,
                "hotels": hotels,
                "total_cost": total_cost,
                "booking_recommendations": gemini_response,
                "estimated_savings": self._calculate_savings(flights, hotels, travel_request)
            }
            
            response_message = f"""
            I've found excellent booking options for your trip to {selected_destination.name}:
            
            FLIGHTS ({len(flights)} options):
            {self._format_flights(flights)}
            
            HOTELS ({len(hotels)} options):
            {self._format_hotels(hotels)}
            
            Total Estimated Cost: ${total_cost:.2f}
            
            {gemini_response}
            """
            
            return self.create_response(
                success=True,
                message=response_message,
                data=booking_summary
            )
            
        except Exception as e:
            return self.create_response(
                success=False,
                message=f"Error processing booking request: {str(e)}",
                data=None
            )
    
    async def _get_flight_options(self, travel_request: TravelRequest, destination: Destination) -> List[Flight]:
        """Get flight options for the trip"""
        origin = "New York"  # Default origin - could be made configurable
        travel_date = travel_request.start_date or date.today() + timedelta(days=30)
        
        # Generate mock flights
        flights = MockDataGenerator.generate_flights(
            origin=origin,
            destination=destination.name,
            date=travel_date,
            num_options=5
        )
        
        # Filter based on budget if needed
        if travel_request.budget == BudgetLevel.BUDGET:
            flights = [f for f in flights if f.price < 500]
        elif travel_request.budget == BudgetLevel.MODERATE:
            flights = [f for f in flights if f.price < 1000]
        
        return flights[:3]  # Return top 3 options
    
    async def _get_hotel_options(self, travel_request: TravelRequest, destination: Destination) -> List[Hotel]:
        """Get hotel options for the trip"""
        # Generate mock hotels
        hotels = MockDataGenerator.generate_hotels(
            destination=destination.name,
            budget=travel_request.budget,
            num_options=5
        )
        
        return hotels[:3]  # Return top 3 options
    
    def _calculate_total_cost(self, flights: List[Flight], hotels: List[Hotel], travel_request: TravelRequest) -> float:
        """Calculate total cost for the trip"""
        if not flights or not hotels:
            return 0.0
        
        # Use cheapest options for cost calculation
        cheapest_flight = min(flights, key=lambda x: x.price)
        cheapest_hotel = min(hotels, key=lambda x: x.price_per_night)
        
        flight_cost = cheapest_flight.price * travel_request.num_travelers
        
        # Calculate hotel cost
        trip_duration = 7  # Default 7 days
        if travel_request.start_date and travel_request.end_date:
            trip_duration = (travel_request.end_date - travel_request.start_date).days
        
        hotel_cost = cheapest_hotel.price_per_night * trip_duration
        
        return flight_cost + hotel_cost
    
    def _calculate_savings(self, flights: List[Flight], hotels: List[Hotel], travel_request: TravelRequest) -> Dict[str, float]:
        """Calculate potential savings"""
        if len(flights) < 2 or len(hotels) < 2:
            return {"flight_savings": 0, "hotel_savings": 0, "total_savings": 0}
        
        # Flight savings
        flight_prices = [f.price for f in flights]
        flight_savings = max(flight_prices) - min(flight_prices)
        
        # Hotel savings
        hotel_prices = [h.price_per_night for h in hotels]
        hotel_savings = (max(hotel_prices) - min(hotel_prices)) * 7  # 7 days
        
        return {
            "flight_savings": flight_savings,
            "hotel_savings": hotel_savings,
            "total_savings": flight_savings + hotel_savings
        }
    
    def _format_flights(self, flights: List[Flight]) -> str:
        """Format flight options for display"""
        formatted = ""
        for i, flight in enumerate(flights, 1):
            formatted += f"""
{i}. {flight.airline} {flight.flight_number}
   {flight.departure_airport} → {flight.arrival_airport}
   {flight.departure_time.strftime('%H:%M')} - {flight.arrival_time.strftime('%H:%M')} ({flight.duration})
   {flight.stops} stops | {flight.cabin_class} | ${flight.price}
"""
        return formatted
    
    def _format_hotels(self, hotels: List[Hotel]) -> str:
        """Format hotel options for display"""
        formatted = ""
        for i, hotel in enumerate(hotels, 1):
            formatted += f"""
{i}. {hotel.name}
   Rating: {hotel.rating}★ | ${hotel.price_per_night}/night
   Location: {hotel.location} ({hotel.distance_from_center})
   Amenities: {', '.join(hotel.amenities[:3])}
"""
        return formatted
    
    async def book_travel(self, booking_data: Dict[str, Any]) -> AgentResponse:
        """Simulate booking the selected travel options"""
        try:
            flight_id = booking_data.get("flight_id")
            hotel_id = booking_data.get("hotel_id")
            passenger_info = booking_data.get("passenger_info", {})
            
            # Simulate booking process
            booking_confirmation = {
                "booking_id": f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "status": "confirmed",
                "flight_booking": {
                    "flight_id": flight_id,
                    "confirmation_number": f"FL{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "status": "confirmed"
                },
                "hotel_booking": {
                    "hotel_id": hotel_id,
                    "confirmation_number": f"HT{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "status": "confirmed"
                },
                "passenger_info": passenger_info,
                "booking_date": datetime.now().isoformat(),
                "total_paid": booking_data.get("total_cost", 0)
            }
            
            return self.create_response(
                success=True,
                message="Booking confirmed successfully! You will receive confirmation emails shortly.",
                data=booking_confirmation
            )
            
        except Exception as e:
            return self.create_response(
                success=False,
                message=f"Error processing booking: {str(e)}",
                data=None
            )
    
    async def get_booking_status(self, booking_id: str) -> AgentResponse:
        """Get the status of a booking"""
        # Simulate booking status check
        status_options = ["confirmed", "pending", "cancelled"]
        
        return self.create_response(
            success=True,
            message=f"Booking {booking_id} status retrieved",
            data={
                "booking_id": booking_id,
                "status": "confirmed",  # Mock status
                "last_updated": datetime.now().isoformat()
            }
        ) 