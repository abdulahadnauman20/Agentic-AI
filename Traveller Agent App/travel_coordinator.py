import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from base_agent import BaseAgent
from destination_agent import DestinationAgent
from booking_agent import BookingAgent
from explore_agent import ExploreAgent
from models import TravelRequest, TravelPlan, AgentResponse, TravelMood, BudgetLevel

class TravelCoordinator(BaseAgent):
    """Main coordinator that orchestrates the travel planning workflow"""
    
    def __init__(self):
        super().__init__(
            name="TravelCoordinator",
            description="Main coordinator that manages the complete travel planning workflow by coordinating between specialized agents."
        )
        
        # Initialize specialized agents
        self.destination_agent = DestinationAgent()
        self.booking_agent = BookingAgent()
        self.explore_agent = ExploreAgent()
        
        # Add coordination tools
        self.add_tool({
            "name": "coordinate_planning",
            "description": "Coordinate the complete travel planning process",
            "parameters": {
                "travel_request": "User's travel request",
                "workflow_steps": "Steps to execute (destination, booking, explore)",
                "preferences": "User preferences and constraints"
            }
        })
        
        self.add_tool({
            "name": "handoff_to_agent",
            "description": "Hand off to a specialized agent",
            "parameters": {
                "agent_name": "Name of the agent to hand off to",
                "request_data": "Data to pass to the agent",
                "context": "Context from previous steps"
            }
        })
        
        # Track planning sessions
        self.active_sessions = {}
    
    async def process_request(self, request: TravelRequest) -> AgentResponse:
        """Process a complete travel planning request"""
        try:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.active_sessions[session_id] = {
                "request": request,
                "status": "started",
                "steps_completed": [],
                "results": {}
            }
            
            self.add_to_history("user", f"New travel planning request: {request.mood.value} trip with {request.budget.value} budget")
            
            # Step 1: Destination Planning
            destination_response = await self._handoff_to_destination_agent(request, session_id)
            if not destination_response.success:
                return destination_response
            
            # Step 2: Booking Planning
            selected_destination = destination_response.data["recommendations"][0]["destination"]
            booking_response = await self._handoff_to_booking_agent(request, selected_destination, session_id)
            if not booking_response.success:
                return booking_response
            
            # Step 3: Exploration Planning
            explore_response = await self._handoff_to_explore_agent(request, selected_destination, session_id)
            if not explore_response.success:
                return explore_response
            
            # Step 4: Create Complete Travel Plan
            travel_plan = await self._create_complete_plan(
                request, destination_response, booking_response, explore_response
            )
            
            # Update session
            self.active_sessions[session_id]["status"] = "completed"
            self.active_sessions[session_id]["results"]["final_plan"] = travel_plan
            
            # Generate final summary using Gemini
            final_summary = await self._generate_final_summary(travel_plan)
            
            return self.create_response(
                success=True,
                message=f"""
🎉 Your complete travel plan is ready!

{destination_response.message}

{booking_response.message}

{explore_response.message}

{final_summary}

Session ID: {session_id}
                """,
                data={
                    "travel_plan": travel_plan,
                    "session_id": session_id,
                    "agents_used": ["DestinationAgent", "BookingAgent", "ExploreAgent"],
                    "total_cost": travel_plan.total_cost
                }
            )
            
        except Exception as e:
            return self.create_response(
                success=False,
                message=f"Error in travel coordination: {str(e)}",
                data=None
            )
    
    async def _handoff_to_destination_agent(self, request: TravelRequest, session_id: str) -> AgentResponse:
        """Hand off to destination agent"""
        self.add_to_history("system", f"Handing off to DestinationAgent for session {session_id}")
        
        response = await self.destination_agent.process_request(request)
        
        if response.success:
            self.active_sessions[session_id]["steps_completed"].append("destination")
            self.active_sessions[session_id]["results"]["destination"] = response.data
        
        return response
    
    async def _handoff_to_booking_agent(self, request: TravelRequest, destination, session_id: str) -> AgentResponse:
        """Hand off to booking agent"""
        self.add_to_history("system", f"Handing off to BookingAgent for session {session_id}")
        
        booking_request = {
            "travel_request": request,
            "destination": destination,
            "preferences": {}
        }
        
        response = await self.booking_agent.process_request(booking_request)
        
        if response.success:
            self.active_sessions[session_id]["steps_completed"].append("booking")
            self.active_sessions[session_id]["results"]["booking"] = response.data
        
        return response
    
    async def _handoff_to_explore_agent(self, request: TravelRequest, destination, session_id: str) -> AgentResponse:
        """Hand off to explore agent"""
        self.add_to_history("system", f"Handing off to ExploreAgent for session {session_id}")
        
        explore_request = {
            "travel_request": request,
            "destination": destination,
            "preferences": {}
        }
        
        response = await self.explore_agent.process_request(explore_request)
        
        if response.success:
            self.active_sessions[session_id]["steps_completed"].append("explore")
            self.active_sessions[session_id]["results"]["explore"] = response.data
        
        return response
    
    async def _create_complete_plan(self, request: TravelRequest, destination_response: AgentResponse, 
                                   booking_response: AgentResponse, explore_response: AgentResponse) -> TravelPlan:
        """Create a complete travel plan from all agent responses"""
        
        # Extract data from responses
        destination = destination_response.data["recommendations"][0]["destination"]
        flights = booking_response.data["flights"]
        hotels = booking_response.data["hotels"]
        attractions = explore_response.data["attractions"]
        restaurants = explore_response.data["restaurants"]
        
        # Calculate total cost
        total_cost = booking_response.data["total_cost"]
        
        # Create travel plan
        travel_plan = TravelPlan(
            request=request,
            destination=destination,
            flights=flights,
            hotel=hotels[0] if hotels else None,  # Select first hotel
            attractions=attractions,
            restaurants=restaurants,
            total_cost=total_cost,
            status="complete"
        )
        
        return travel_plan
    
    async def _generate_final_summary(self, travel_plan: TravelPlan) -> str:
        """Generate a final summary using Gemini"""
        summary_prompt = f"""
        Create a compelling final summary for this travel plan:
        
        Destination: {travel_plan.destination.name}, {travel_plan.destination.country}
        Travel Style: {travel_plan.request.mood.value}
        Budget: {travel_plan.request.budget.value}
        Duration: {self._calculate_duration(travel_plan.request)} days
        Total Cost: ${travel_plan.total_cost:.2f}
        
        Highlights:
        - {len(travel_plan.flights)} flight options available
        - {len(travel_plan.attractions)} attractions recommended
        - {len(travel_plan.restaurants)} restaurants suggested
        
        Please create an exciting, personalized summary that makes the user excited about their trip.
        Include key highlights and what makes this destination special for their travel style.
        """
        
        return await self.call_gemini(summary_prompt)
    
    def _calculate_duration(self, request: TravelRequest) -> int:
        """Calculate trip duration"""
        if request.start_date and request.end_date:
            return (request.end_date - request.start_date).days
        return 7
    
    async def get_session_status(self, session_id: str) -> AgentResponse:
        """Get the status of a planning session"""
        if session_id not in self.active_sessions:
            return self.create_response(
                success=False,
                message=f"Session {session_id} not found",
                data=None
            )
        
        session = self.active_sessions[session_id]
        return self.create_response(
            success=True,
            message=f"Session {session_id} status: {session['status']}",
            data=session
        )
    
    async def modify_plan(self, session_id: str, modifications: Dict[str, Any]) -> AgentResponse:
        """Modify an existing travel plan"""
        if session_id not in self.active_sessions:
            return self.create_response(
                success=False,
                message=f"Session {session_id} not found",
                data=None
            )
        
        session = self.active_sessions[session_id]
        
        # Apply modifications
        if "destination" in modifications:
            # Re-run destination agent with new preferences
            request = session["request"]
            request.destination_preferences.extend(modifications["destination"])
            destination_response = await self._handoff_to_destination_agent(request, session_id)
            
            if destination_response.success:
                # Update session with new destination
                session["results"]["destination"] = destination_response.data
                session["status"] = "modified"
        
        return self.create_response(
            success=True,
            message=f"Plan modified successfully for session {session_id}",
            data=session
        )
    
    def get_coordinator_stats(self) -> Dict[str, Any]:
        """Get coordinator statistics"""
        total_sessions = len(self.active_sessions)
        completed_sessions = len([s for s in self.active_sessions.values() if s["status"] == "completed"])
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "active_sessions": total_sessions - completed_sessions,
            "success_rate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
            "agents_available": [
                self.destination_agent.name,
                self.booking_agent.name,
                self.explore_agent.name
            ]
        }
    
    async def emergency_handoff(self, agent_name: str, request_data: Dict[str, Any]) -> AgentResponse:
        """Emergency handoff to a specific agent"""
        try:
            if agent_name == "DestinationAgent":
                return await self.destination_agent.process_request(request_data)
            elif agent_name == "BookingAgent":
                return await self.booking_agent.process_request(request_data)
            elif agent_name == "ExploreAgent":
                return await self.explore_agent.process_request(request_data)
            else:
                return self.create_response(
                    success=False,
                    message=f"Unknown agent: {agent_name}",
                    data=None
                )
        except Exception as e:
            return self.create_response(
                success=False,
                message=f"Emergency handoff failed: {str(e)}",
                data=None
            ) 