#!/usr/bin/env python3
"""
Travel Agent System - Demo Script
Quick demonstration of the travel agent system with predefined examples
"""

import asyncio
import json
from datetime import date, timedelta
from typing import Dict, Any

from config import Config
from models import TravelRequest, TravelMood, BudgetLevel
from travel_coordinator import TravelCoordinator
from destination_agent import DestinationAgent
from booking_agent import BookingAgent
from explore_agent import ExploreAgent

class TravelAgentDemo:
    """Demo class for showcasing the travel agent system"""
    
    def __init__(self):
        self.coordinator = TravelCoordinator()
        self.destination_agent = DestinationAgent()
        self.booking_agent = BookingAgent()
        self.explore_agent = ExploreAgent()
    
    async def run_demo(self):
        """Run the complete demo"""
        print("🌍 AI Travel Agent System - Demo Mode")
        print("=" * 50)
        
        # Check configuration
        if not Config.validate_config():
            print("⚠️  Running in demo mode without Gemini API")
            print("Set GEMINI_API_KEY for full AI capabilities\n")
        
        # Demo examples
        examples = [
            {
                "name": "Adventure Seeker",
                "description": "Mountain climbing and outdoor activities",
                "request": TravelRequest(
                    user_name="Alex",
                    destination_preferences=["mountains", "hiking"],
                    mood=TravelMood.ADVENTURE,
                    budget=BudgetLevel.MODERATE,
                    start_date=date.today() + timedelta(days=30),
                    end_date=date.today() + timedelta(days=37),
                    num_travelers=2,
                    special_requirements=["outdoor activities", "scenic views"]
                )
            },
            {
                "name": "Culture Enthusiast",
                "description": "Museums, historical sites, and local culture",
                "request": TravelRequest(
                    user_name="Maria",
                    destination_preferences=["museums", "history"],
                    mood=TravelMood.CULTURE,
                    budget=BudgetLevel.LUXURY,
                    start_date=date.today() + timedelta(days=45),
                    end_date=date.today() + timedelta(days=52),
                    num_travelers=1,
                    special_requirements=["guided tours", "cultural experiences"]
                )
            },
            {
                "name": "Beach Relaxation",
                "description": "Tropical paradise and relaxation",
                "request": TravelRequest(
                    user_name="Sarah",
                    destination_preferences=["beach", "tropical"],
                    mood=TravelMood.RELAXATION,
                    budget=BudgetLevel.MODERATE,
                    start_date=date.today() + timedelta(days=60),
                    end_date=date.today() + timedelta(days=67),
                    num_travelers=3,
                    special_requirements=["spa", "ocean view"]
                )
            },
            {
                "name": "Food Explorer",
                "description": "Culinary adventures and local cuisine",
                "request": TravelRequest(
                    user_name="Chef Mike",
                    destination_preferences=["food", "cuisine"],
                    mood=TravelMood.FOOD,
                    budget=BudgetLevel.MODERATE,
                    start_date=date.today() + timedelta(days=15),
                    end_date=date.today() + timedelta(days=22),
                    num_travelers=2,
                    special_requirements=["cooking classes", "local markets"]
                )
            }
        ]
        
        print("Available Demo Examples:")
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example['name']} - {example['description']}")
        
        print("\n5. 🧪 Test Individual Agents")
        print("6. 🎯 Quick Custom Plan")
        print("7. 📊 System Overview")
        print("8. 🚪 Exit")
        
        while True:
            try:
                choice = input("\nSelect demo option (1-8): ").strip()
                
                if choice == "1":
                    await self._run_example_demo(examples[0])
                elif choice == "2":
                    await self._run_example_demo(examples[1])
                elif choice == "3":
                    await self._run_example_demo(examples[2])
                elif choice == "4":
                    await self._run_example_demo(examples[3])
                elif choice == "5":
                    await self._test_individual_agents()
                elif choice == "6":
                    await self._quick_custom_plan()
                elif choice == "7":
                    await self._system_overview()
                elif choice == "8":
                    print("👋 Demo completed!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted!")
                break
            except Exception as e:
                print(f"❌ Demo error: {str(e)}")
    
    async def _run_example_demo(self, example: Dict[str, Any]):
        """Run a specific example demo"""
        print(f"\n🎯 Running Demo: {example['name']}")
        print(f"Description: {example['description']}")
        print("-" * 50)
        
        request = example['request']
        print(f"User: {request.user_name}")
        print(f"Mood: {request.mood.value}")
        print(f"Budget: {request.budget.value}")
        print(f"Preferences: {', '.join(request.destination_preferences)}")
        print(f"Requirements: {', '.join(request.special_requirements)}")
        print(f"Travelers: {request.num_travelers}")
        print(f"Dates: {request.start_date} to {request.end_date}")
        
        print("\n🚀 Creating complete travel plan...")
        print("(This demonstrates the full agent coordination workflow)")
        
        # Run complete planning workflow
        response = await self.coordinator.process_request(request)
        
        if response.success:
            print("\n" + "=" * 60)
            print("✅ COMPLETE TRAVEL PLAN CREATED!")
            print("=" * 60)
            print(response.message)
            print("=" * 60)
            
            # Show session details
            session_id = response.data["session_id"]
            print(f"\n📊 Session ID: {session_id}")
            print(f"Total Cost: ${response.data['total_cost']:.2f}")
            print(f"Agents Used: {', '.join(response.data['agents_used'])}")
        else:
            print(f"\n❌ Error: {response.message}")
    
    async def _test_individual_agents(self):
        """Test individual agents separately"""
        print("\n🧪 Individual Agent Testing")
        print("-" * 30)
        print("1. DestinationAgent Test")
        print("2. BookingAgent Test")
        print("3. ExploreAgent Test")
        print("4. Back to main menu")
        
        choice = input("Select agent to test (1-4): ").strip()
        
        # Create a sample request for testing
        sample_request = TravelRequest(
            user_name="Demo User",
            destination_preferences=["culture", "history"],
            mood=TravelMood.CULTURE,
            budget=BudgetLevel.MODERATE,
            num_travelers=2
        )
        
        try:
            if choice == "1":
                print("\n🎯 Testing DestinationAgent...")
                response = await self.destination_agent.process_request(sample_request)
                print(response.message)
                
            elif choice == "2":
                print("\n✈️ Testing BookingAgent...")
                # First get a destination
                dest_response = await self.destination_agent.process_request(sample_request)
                if dest_response.success:
                    destination = dest_response.data["recommendations"][0]["destination"]
                    booking_request = {
                        "travel_request": sample_request,
                        "destination": destination
                    }
                    response = await self.booking_agent.process_request(booking_request)
                    print(response.message)
                else:
                    print("❌ Could not get destination for booking test")
                    
            elif choice == "3":
                print("\n🏛️ Testing ExploreAgent...")
                # First get a destination
                dest_response = await self.destination_agent.process_request(sample_request)
                if dest_response.success:
                    destination = dest_response.data["recommendations"][0]["destination"]
                    explore_request = {
                        "travel_request": sample_request,
                        "destination": destination
                    }
                    response = await self.explore_agent.process_request(explore_request)
                    print(response.message)
                else:
                    print("❌ Could not get destination for explore test")
                    
            elif choice == "4":
                return
            else:
                print("❌ Invalid choice.")
                
        except Exception as e:
            print(f"❌ Agent test error: {str(e)}")
    
    async def _quick_custom_plan(self):
        """Create a quick custom travel plan"""
        print("\n🎯 Quick Custom Travel Plan")
        print("-" * 30)
        
        # Get basic preferences
        name = input("Your name (or press Enter for default): ").strip() or "Traveler"
        
        print("\nTravel mood:")
        for i, mood in enumerate(TravelMood, 1):
            print(f"{i}. {mood.value.title()}")
        mood_choice = input("Choose mood (1-8, or press Enter for default): ").strip()
        
        try:
            mood = list(TravelMood)[int(mood_choice) - 1] if mood_choice else TravelMood.ADVENTURE
        except (ValueError, IndexError):
            mood = TravelMood.ADVENTURE
        
        print("\nBudget level:")
        for i, budget in enumerate(BudgetLevel, 1):
            print(f"{i}. {budget.value.title()}")
        budget_choice = input("Choose budget (1-3, or press Enter for default): ").strip()
        
        try:
            budget = list(BudgetLevel)[int(budget_choice) - 1] if budget_choice else BudgetLevel.MODERATE
        except (ValueError, IndexError):
            budget = BudgetLevel.MODERATE
        
        # Create request
        request = TravelRequest(
            user_name=name,
            destination_preferences=[],
            mood=mood,
            budget=budget,
            num_travelers=1
        )
        
        print(f"\n🚀 Creating {mood.value} travel plan with {budget.value} budget...")
        
        response = await self.coordinator.process_request(request)
        
        if response.success:
            print("\n" + "=" * 50)
            print("✅ QUICK PLAN CREATED!")
            print("=" * 50)
            print(response.message)
            print("=" * 50)
        else:
            print(f"\n❌ Error: {response.message}")
    
    async def _system_overview(self):
        """Show system overview and statistics"""
        print("\n📊 System Overview")
        print("-" * 20)
        
        # Get coordinator stats
        stats = self.coordinator.get_coordinator_stats()
        
        print(f"🤖 Total Agents: {len(stats['agents_available'])}")
        print(f"📈 Total Sessions: {stats['total_sessions']}")
        print(f"✅ Completed Sessions: {stats['completed_sessions']}")
        print(f"🔄 Active Sessions: {stats['active_sessions']}")
        print(f"📊 Success Rate: {stats['success_rate']:.1f}%")
        
        print("\n🤖 Agent Details:")
        for agent_name in stats['agents_available']:
            if hasattr(self.coordinator, f"{agent_name.lower()}"):
                agent = getattr(self.coordinator, f"{agent_name.lower()}")
                agent_info = agent.get_agent_info()
                print(f"  • {agent_info['name']}")
                print(f"    Description: {agent_info['description']}")
                print(f"    Tools: {len(agent_info['tools'])}")
                print(f"    History: {agent_info['conversation_history_length']} messages")
        
        print("\n🔧 Configuration:")
        print(f"  • Gemini Model: {Config.GEMINI_MODEL}")
        print(f"  • Max Retries: {Config.MAX_RETRIES}")
        print(f"  • Timeout: {Config.TIMEOUT_SECONDS}s")
        print(f"  • Mock Data: {'Enabled' if Config.MOCK_FLIGHTS_ENABLED else 'Disabled'}")
        
        print("\n📋 Available Destinations:")
        destinations = [
            "Bali, Indonesia (Relaxation, Culture, Beach)",
            "Tokyo, Japan (Urban, Culture, Food)",
            "Paris, France (Culture, Food, Urban)",
            "New York, USA (Urban, Culture, Food)",
            "Swiss Alps, Switzerland (Adventure, Mountains, Nature)"
        ]
        for dest in destinations:
            print(f"  • {dest}")
    
    async def _performance_test(self):
        """Run a quick performance test"""
        print("\n⚡ Performance Test")
        print("-" * 20)
        
        import time
        
        # Test destination agent speed
        start_time = time.time()
        request = TravelRequest(
            user_name="Performance Test",
            mood=TravelMood.ADVENTURE,
            budget=BudgetLevel.MODERATE
        )
        
        response = await self.destination_agent.process_request(request)
        end_time = time.time()
        
        print(f"DestinationAgent Response Time: {end_time - start_time:.2f} seconds")
        print(f"Success: {response.success}")
        
        if response.success:
            print(f"Destinations Found: {len(response.data['recommendations'])}")

def main():
    """Main entry point for demo"""
    demo = TravelAgentDemo()
    
    try:
        asyncio.run(demo.run_demo())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted!")
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")

if __name__ == "__main__":
    main() 