import asyncio
from typing import List, Dict, Any
from datetime import datetime

from base_agent import BaseAgent
from models import TravelRequest, Destination, TravelMood, BudgetLevel, AgentResponse
from mock_data import MockDataGenerator

class DestinationAgent(BaseAgent):
    """Agent specialized in suggesting travel destinations based on user preferences"""
    
    def __init__(self):
        super().__init__(
            name="DestinationAgent",
            description="Specialized in analyzing user preferences and suggesting the best travel destinations based on mood, budget, and interests."
        )
        
        # Add tools specific to destination finding
        self.add_tool({
            "name": "analyze_preferences",
            "description": "Analyze user preferences to understand travel needs",
            "parameters": {
                "mood": "Travel mood (adventure, relaxation, culture, etc.)",
                "budget": "Budget level (budget, moderate, luxury)",
                "interests": "List of user interests",
                "constraints": "Any travel constraints or requirements"
            }
        })
        
        self.add_tool({
            "name": "suggest_destinations",
            "description": "Suggest destinations based on analyzed preferences",
            "parameters": {
                "mood": "Travel mood",
                "budget": "Budget level",
                "season": "Preferred travel season",
                "duration": "Trip duration"
            }
        })
        
        # Load available destinations
        self.available_destinations = MockDataGenerator.generate_destinations()
    
    async def process_request(self, request: TravelRequest) -> AgentResponse:
        """Process a travel request and suggest destinations"""
        try:
            # Add request to conversation history
            self.add_to_history("user", f"Looking for destinations with mood: {request.mood.value}, budget: {request.budget.value}")
            
            # Analyze the request using Gemini
            analysis_prompt = f"""
            Analyze this travel request and suggest the best destinations:
            
            User: {request.user_name}
            Mood: {request.mood.value}
            Budget: {request.budget.value}
            Preferences: {request.destination_preferences}
            Special Requirements: {request.special_requirements}
            Number of Travelers: {request.num_travelers}
            
            Available destinations: {[d.name for d in self.available_destinations]}
            
            Please analyze the user's preferences and suggest 3-5 destinations that would be perfect for them.
            Consider mood compatibility, budget suitability, and any special requirements.
            """
            
            gemini_response = await self.call_gemini(analysis_prompt)
            self.add_to_history("assistant", gemini_response)
            
            # Filter destinations based on criteria
            suggested_destinations = self._filter_destinations(request)
            
            # Create detailed recommendations
            recommendations = []
            for dest in suggested_destinations[:5]:  # Top 5 recommendations
                recommendation = {
                    "destination": dest,
                    "match_score": self._calculate_match_score(dest, request),
                    "reasoning": self._generate_reasoning(dest, request),
                    "best_time_to_visit": dest.best_time_to_visit,
                    "estimated_cost": self._estimate_cost(dest, request)
                }
                recommendations.append(recommendation)
            
            # Sort by match score
            recommendations.sort(key=lambda x: x["match_score"], reverse=True)
            
            response_message = f"""
            Based on your preferences for {request.mood.value} travel with a {request.budget.value} budget, 
            I've found {len(recommendations)} perfect destinations for you:
            
            {self._format_recommendations(recommendations)}
            
            {gemini_response}
            """
            
            return self.create_response(
                success=True,
                message=response_message,
                data={
                    "recommendations": recommendations,
                    "analysis": gemini_response,
                    "total_destinations_considered": len(self.available_destinations)
                }
            )
            
        except Exception as e:
            return self.create_response(
                success=False,
                message=f"Error processing destination request: {str(e)}",
                data=None
            )
    
    def _filter_destinations(self, request: TravelRequest) -> List[Destination]:
        """Filter destinations based on user preferences"""
        filtered = []
        
        for dest in self.available_destinations:
            # Check mood compatibility
            if request.mood in dest.mood_suitability:
                # Check budget compatibility
                if self._is_budget_compatible(dest.budget_range, request.budget):
                    filtered.append(dest)
        
        # If no exact matches, include some close matches
        if not filtered:
            for dest in self.available_destinations:
                if self._calculate_match_score(dest, request) > 0.3:
                    filtered.append(dest)
        
        return filtered
    
    def _is_budget_compatible(self, dest_budget: BudgetLevel, user_budget: BudgetLevel) -> bool:
        """Check if destination budget is compatible with user budget"""
        budget_hierarchy = {
            BudgetLevel.BUDGET: 1,
            BudgetLevel.MODERATE: 2,
            BudgetLevel.LUXURY: 3
        }
        
        # User can afford destinations at their budget level or lower
        return budget_hierarchy[dest_budget] <= budget_hierarchy[user_budget]
    
    def _calculate_match_score(self, destination: Destination, request: TravelRequest) -> float:
        """Calculate how well a destination matches the user's preferences"""
        score = 0.0
        
        # Mood compatibility (40% weight)
        if request.mood in destination.mood_suitability:
            score += 0.4
        
        # Budget compatibility (30% weight)
        if self._is_budget_compatible(destination.budget_range, request.budget):
            score += 0.3
        
        # Preference matching (20% weight)
        for preference in request.destination_preferences:
            if preference.lower() in destination.name.lower() or preference.lower() in destination.country.lower():
                score += 0.1
        
        # Special requirements (10% weight)
        for requirement in request.special_requirements:
            if any(req.lower() in activity.lower() for activity in destination.activities for req in [requirement]):
                score += 0.05
        
        return min(score, 1.0)
    
    def _generate_reasoning(self, destination: Destination, request: TravelRequest) -> str:
        """Generate reasoning for why this destination is recommended"""
        reasons = []
        
        if request.mood in destination.mood_suitability:
            reasons.append(f"Perfect for {request.mood.value} travel")
        
        if self._is_budget_compatible(destination.budget_range, request.budget):
            reasons.append(f"Fits your {request.budget.value} budget")
        
        if destination.activities:
            reasons.append(f"Offers activities like {', '.join(destination.activities[:3])}")
        
        return "; ".join(reasons) if reasons else "Good overall match for your preferences"
    
    def _estimate_cost(self, destination: Destination, request: TravelRequest) -> Dict[str, float]:
        """Estimate travel costs for the destination"""
        base_costs = {
            BudgetLevel.BUDGET: {"accommodation": 50, "food": 30, "activities": 20},
            BudgetLevel.MODERATE: {"accommodation": 150, "food": 60, "activities": 50},
            BudgetLevel.LUXURY: {"accommodation": 400, "food": 120, "activities": 100}
        }
        
        daily_costs = base_costs[destination.budget_range]
        trip_duration = 7  # Default 7 days
        
        if request.start_date and request.end_date:
            trip_duration = (request.end_date - request.start_date).days
        
        total_cost = sum(daily_costs.values()) * trip_duration * request.num_travelers
        
        return {
            "daily_cost": sum(daily_costs.values()),
            "total_cost": total_cost,
            "cost_breakdown": daily_costs
        }
    
    def _format_recommendations(self, recommendations: List[Dict]) -> str:
        """Format recommendations for display"""
        formatted = ""
        for i, rec in enumerate(recommendations, 1):
            dest = rec["destination"]
            formatted += f"""
{i}. {dest.name}, {dest.country}
   Match Score: {rec['match_score']:.1%}
   Reasoning: {rec['reasoning']}
   Best Time: {rec['best_time_to_visit']}
   Estimated Daily Cost: ${rec['estimated_cost']['daily_cost']}
   Description: {dest.description}
"""
        return formatted
    
    async def get_destination_details(self, destination_name: str) -> AgentResponse:
        """Get detailed information about a specific destination"""
        for dest in self.available_destinations:
            if dest.name.lower() == destination_name.lower():
                return self.create_response(
                    success=True,
                    message=f"Detailed information for {dest.name}",
                    data={"destination": dest}
                )
        
        return self.create_response(
            success=False,
            message=f"Destination '{destination_name}' not found",
            data=None
        ) 