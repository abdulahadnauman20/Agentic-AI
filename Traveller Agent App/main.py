#!/usr/bin/env python3
"""
Travel Agent System - Main Application
A comprehensive travel planning system using specialized AI agents with Gemini API
"""

import asyncio
import json
from datetime import date, datetime
from typing import Dict, Any

from config import Config
from models import TravelRequest, TravelMood, BudgetLevel
from travel_coordinator import TravelCoordinator

class TravelAgentApp:
    """Main application for the Travel Agent System"""
    
    def __init__(self):
        self.coordinator = TravelCoordinator()
        self.current_session = None
    
    async def run(self):
        """Run the main application"""
        print("🌍 Welcome to the AI Travel Agent System!")
        print("=" * 50)
        
        # Check configuration
        if not Config.validate_config():
            print("\n⚠️  Running in demo mode without Gemini API")
            print("Set GEMINI_API_KEY environment variable for full AI capabilities")
        
        while True:
            try:
                await self._show_main_menu()
                choice = input("\nEnter your choice (1-6): ").strip()
                
                if choice == "1":
                    await self._create_travel_plan()
                elif choice == "2":
                    await self._view_session_status()
                elif choice == "3":
                    await self._modify_plan()
                elif choice == "4":
                    await self._show_system_stats()
                elif choice == "5":
                    await self._demo_agents()
                elif choice == "6":
                    print("\n👋 Thank you for using the AI Travel Agent System!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {str(e)}")
    
    async def _show_main_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 50)
        print("🏖️  AI TRAVEL AGENT SYSTEM")
        print("=" * 50)
        print("1. 🎯 Create New Travel Plan")
        print("2. 📊 View Session Status")
        print("3. ✏️  Modify Existing Plan")
        print("4. 📈 System Statistics")
        print("5. 🧪 Demo Individual Agents")
        print("6. 🚪 Exit")
        print("=" * 50)
    
    async def _create_travel_plan(self):
        """Create a new travel plan"""
        print("\n🎯 Creating New Travel Plan")
        print("-" * 30)
        
        # Get user information
        user_name = input("Enter your name: ").strip() or "Traveler"
        
        # Get travel mood
        print("\nWhat's your travel mood?")
        for i, mood in enumerate(TravelMood, 1):
            print(f"{i}. {mood.value.title()}")
        
        mood_choice = input("Choose your mood (1-8): ").strip()
        try:
            mood = list(TravelMood)[int(mood_choice) - 1]
        except (ValueError, IndexError):
            mood = TravelMood.ADVENTURE
            print(f"Using default mood: {mood.value}")
        
        # Get budget
        print("\nWhat's your budget level?")
        for i, budget in enumerate(BudgetLevel, 1):
            print(f"{i}. {budget.value.title()}")
        
        budget_choice = input("Choose your budget (1-3): ").strip()
        try:
            budget = list(BudgetLevel)[int(budget_choice) - 1]
        except (ValueError, IndexError):
            budget = BudgetLevel.MODERATE
            print(f"Using default budget: {budget.value}")
        
        # Get destination preferences
        print("\nAny specific destinations in mind? (comma-separated, or press Enter to skip)")
        preferences_input = input("Destinations: ").strip()
        destination_preferences = [p.strip() for p in preferences_input.split(",") if p.strip()]
        
        # Get special requirements
        print("\nAny special requirements? (comma-separated, or press Enter to skip)")
        requirements_input = input("Requirements: ").strip()
        special_requirements = [r.strip() for r in requirements_input.split(",") if r.strip()]
        
        # Get travel dates
        print("\nTravel dates (optional):")
        start_date_str = input("Start date (YYYY-MM-DD, or press Enter to skip): ").strip()
        end_date_str = input("End date (YYYY-MM-DD, or press Enter to skip): ").strip()
        
        start_date = None
        end_date = None
        if start_date_str and end_date_str:
            try:
                start_date = date.fromisoformat(start_date_str)
                end_date = date.fromisoformat(end_date_str)
            except ValueError:
                print("⚠️  Invalid date format. Using default dates.")
        
        # Get number of travelers
        travelers_input = input("Number of travelers (default: 1): ").strip()
        num_travelers = int(travelers_input) if travelers_input.isdigit() else 1
        
        # Create travel request
        travel_request = TravelRequest(
            user_name=user_name,
            destination_preferences=destination_preferences,
            mood=mood,
            budget=budget,
            start_date=start_date,
            end_date=end_date,
            num_travelers=num_travelers,
            special_requirements=special_requirements
        )
        
        print(f"\n🚀 Creating your {mood.value} travel plan with {budget.value} budget...")
        print("This may take a few moments as our AI agents work together...")
        
        # Process the request
        response = await self.coordinator.process_request(travel_request)
        
        if response.success:
            self.current_session = response.data["session_id"]
            print("\n" + "=" * 60)
            print("✅ TRAVEL PLAN CREATED SUCCESSFULLY!")
            print("=" * 60)
            print(response.message)
            print("=" * 60)
        else:
            print(f"\n❌ Error creating travel plan: {response.message}")
    
    async def _view_session_status(self):
        """View the status of a planning session"""
        if not self.current_session:
            print("\n❌ No active session. Create a travel plan first.")
            return
        
        print(f"\n📊 Session Status: {self.current_session}")
        response = await self.coordinator.get_session_status(self.current_session)
        
        if response.success:
            session_data = response.data
            print(f"Status: {session_data['status']}")
            print(f"Steps completed: {', '.join(session_data['steps_completed'])}")
            if 'final_plan' in session_data['results']:
                plan = session_data['results']['final_plan']
                print(f"Destination: {plan.destination.name}")
                print(f"Total cost: ${plan.total_cost:.2f}")
        else:
            print(f"❌ Error: {response.message}")
    
    async def _modify_plan(self):
        """Modify an existing travel plan"""
        if not self.current_session:
            print("\n❌ No active session. Create a travel plan first.")
            return
        
        print(f"\n✏️  Modifying Plan: {self.current_session}")
        print("What would you like to modify?")
        print("1. Add destination preferences")
        print("2. Change budget")
        print("3. Add special requirements")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        modifications = {}
        if choice == "1":
            new_prefs = input("Enter new destination preferences (comma-separated): ").strip()
            if new_prefs:
                modifications["destination"] = [p.strip() for p in new_prefs.split(",")]
        elif choice == "2":
            print("New budget level:")
            for i, budget in enumerate(BudgetLevel, 1):
                print(f"{i}. {budget.value.title()}")
            budget_choice = input("Choose new budget (1-3): ").strip()
            try:
                new_budget = list(BudgetLevel)[int(budget_choice) - 1]
                modifications["budget"] = new_budget
            except (ValueError, IndexError):
                print("❌ Invalid budget choice.")
                return
        elif choice == "3":
            new_reqs = input("Enter new special requirements (comma-separated): ").strip()
            if new_reqs:
                modifications["requirements"] = [r.strip() for r in new_reqs.split(",")]
        else:
            print("❌ Invalid choice.")
            return
        
        if modifications:
            response = await self.coordinator.modify_plan(self.current_session, modifications)
            if response.success:
                print("✅ Plan modified successfully!")
            else:
                print(f"❌ Error modifying plan: {response.message}")
    
    async def _show_system_stats(self):
        """Show system statistics"""
        print("\n📈 System Statistics")
        print("-" * 20)
        
        stats = self.coordinator.get_coordinator_stats()
        print(f"Total sessions: {stats['total_sessions']}")
        print(f"Completed sessions: {stats['completed_sessions']}")
        print(f"Active sessions: {stats['active_sessions']}")
        print(f"Success rate: {stats['success_rate']:.1f}%")
        print(f"Available agents: {', '.join(stats['agents_available'])}")
        
        # Show agent info
        print("\n🤖 Agent Information:")
        for agent_name in stats['agents_available']:
            if hasattr(self.coordinator, f"{agent_name.lower()}"):
                agent = getattr(self.coordinator, f"{agent_name.lower()}")
                agent_info = agent.get_agent_info()
                print(f"  {agent_info['name']}: {agent_info['description']}")
    
    async def _demo_agents(self):
        """Demo individual agents"""
        print("\n🧪 Agent Demo Mode")
        print("-" * 20)
        print("1. DestinationAgent Demo")
        print("2. BookingAgent Demo")
        print("3. ExploreAgent Demo")
        
        choice = input("Choose agent to demo (1-3): ").strip()
        
        # Create a sample travel request
        sample_request = TravelRequest(
            user_name="Demo User",
            destination_preferences=["beach", "culture"],
            mood=TravelMood.RELAXATION,
            budget=BudgetLevel.MODERATE,
            num_travelers=2
        )
        
        try:
            if choice == "1":
                print("\n🎯 Testing DestinationAgent...")
                response = await self.coordinator.destination_agent.process_request(sample_request)
                print(response.message)
            elif choice == "2":
                print("\n✈️  Testing BookingAgent...")
                # Need a destination for booking agent
                dest_response = await self.coordinator.destination_agent.process_request(sample_request)
                if dest_response.success:
                    destination = dest_response.data["recommendations"][0]["destination"]
                    booking_request = {
                        "travel_request": sample_request,
                        "destination": destination
                    }
                    response = await self.coordinator.booking_agent.process_request(booking_request)
                    print(response.message)
            elif choice == "3":
                print("\n🏛️  Testing ExploreAgent...")
                # Need a destination for explore agent
                dest_response = await self.coordinator.destination_agent.process_request(sample_request)
                if dest_response.success:
                    destination = dest_response.data["recommendations"][0]["destination"]
                    explore_request = {
                        "travel_request": sample_request,
                        "destination": destination
                    }
                    response = await self.coordinator.explore_agent.process_request(explore_request)
                    print(response.message)
            else:
                print("❌ Invalid choice.")
        except Exception as e:
            print(f"❌ Demo error: {str(e)}")

def main():
    """Main entry point"""
    app = TravelAgentApp()
    
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Application error: {str(e)}")

if __name__ == "__main__":
    main() 