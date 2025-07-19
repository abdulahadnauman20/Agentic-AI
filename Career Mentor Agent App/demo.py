"""
Demo script for Career Mentor Agent
This script demonstrates the core functionality without requiring the Streamlit interface.
"""

import os
import sys
from typing import Dict, List, Any

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import CareerAgent, SkillAgent, JobAgent, AgentOrchestrator
from tools import CareerTools
import config

def demo_career_agent():
    """Demonstrate CareerAgent functionality."""
    print("🎯 CareerAgent Demo")
    print("=" * 50)
    
    # Initialize agent
    career_agent = CareerAgent()
    
    # Sample user profile
    interests = ["programming", "data analysis", "problem solving"]
    skills = ["Python", "basic statistics", "communication"]
    experience_level = "beginner"
    
    print(f"User Profile:")
    print(f"  Interests: {', '.join(interests)}")
    print(f"  Skills: {', '.join(skills)}")
    print(f"  Experience: {experience_level}")
    print()
    
    # Get career recommendations
    print("Getting career recommendations...")
    recommendations = career_agent.recommend_careers(interests, skills, experience_level)
    print(f"Agent: {recommendations['agent']}")
    print(f"Recommendations: {recommendations['recommendations']}")
    print()

def demo_skill_agent():
    """Demonstrate SkillAgent functionality."""
    print("📚 SkillAgent Demo")
    print("=" * 50)
    
    # Initialize agent
    skill_agent = SkillAgent()
    
    # Generate skill roadmap
    career_field = "Software Development"
    experience_level = "beginner"
    
    print(f"Generating skill roadmap for {career_field} ({experience_level} level)...")
    roadmap = skill_agent.generate_skill_roadmap(career_field, experience_level)
    
    print(f"Agent: {roadmap['agent']}")
    print(f"Career Field: {roadmap['career_field']}")
    print(f"Experience Level: {roadmap['experience_level']}")
    
    # Display roadmap phases
    roadmap_data = roadmap['roadmap']['roadmap']
    if 'beginner' in roadmap_data:
        beginner_phase = roadmap_data['beginner']
        print(f"\n{beginner_phase['phase']}:")
        print("Skills:")
        for skill in beginner_phase['skills'][:3]:  # Show first 3 skills
            print(f"  - {skill}")
        print("Projects:")
        for project in beginner_phase['projects'][:2]:  # Show first 2 projects
            print(f"  - {project}")
    print()

def demo_job_agent():
    """Demonstrate JobAgent functionality."""
    print("💼 JobAgent Demo")
    print("=" * 50)
    
    # Initialize agent
    job_agent = JobAgent()
    
    # Get job insights
    career_field = "Data Science"
    
    print(f"Getting job insights for {career_field}...")
    insights = job_agent.get_job_insights(career_field)
    
    print(f"Agent: {insights['agent']}")
    print(f"Career Field: {insights['career_field']}")
    
    # Display job roles
    job_data = insights['job_insights']
    print("\nEntry Level Roles:")
    for role in job_data['entry_level_roles'][:3]:  # Show first 3
        print(f"  - {role}")
    
    print("\nMid Level Roles:")
    for role in job_data['mid_level_roles'][:3]:  # Show first 3
        print(f"  - {role}")
    
    print(f"\nSalary Ranges: {job_data['salary_ranges']}")
    print()

def demo_tools():
    """Demonstrate CareerTools functionality."""
    print("🛠️ CareerTools Demo")
    print("=" * 50)
    
    # Test career roadmap tool
    career_field = "Software Development"
    experience_level = "beginner"
    
    print(f"Testing get_career_roadmap() for {career_field}...")
    roadmap = CareerTools.get_career_roadmap(career_field, experience_level)
    
    print(f"Career Field: {roadmap['career_field']}")
    print(f"Experience Level: {roadmap['experience_level']}")
    print(f"Next Steps: {len(roadmap['next_steps'])} steps provided")
    
    # Test skill assessment
    interests = ["programming", "data", "design"]
    current_skills = ["Python", "communication"]
    
    print(f"\nTesting skill assessment...")
    assessment = CareerTools.get_skill_assessment(interests, current_skills)
    
    print(f"Recommended Careers: {assessment['recommended_careers'][:3]}")  # Show first 3
    print(f"Skill Gaps: {len(assessment['skill_gaps'])} gaps identified")
    print()

def demo_orchestrator():
    """Demonstrate AgentOrchestrator functionality."""
    print("🎭 AgentOrchestrator Demo")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    # Sample user profile
    user_profile = {
        'interests': ['programming', 'data analysis', 'machine learning'],
        'skills': ['Python', 'basic statistics', 'SQL'],
        'experience_level': 'beginner',
        'goals': ['become a data scientist', 'work in tech industry']
    }
    
    print("Getting comprehensive guidance...")
    guidance = orchestrator.get_comprehensive_guidance(user_profile)
    
    print("Comprehensive guidance generated with:")
    print(f"  - Career recommendations from {guidance['career_recommendations']['agent']}")
    print(f"  - Skill roadmap from {guidance['skill_roadmap']['agent']}")
    print(f"  - Job insights from {guidance['job_insights']['agent']}")
    print(f"  - Summary: {guidance['summary']}")
    print()

def demo_chat():
    """Demonstrate chat functionality."""
    print("💬 Chat Demo")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    # Sample queries
    queries = [
        "What career paths are good for someone interested in programming?",
        "What skills do I need to become a data scientist?",
        "What are the job opportunities in software development?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        response = orchestrator.process_user_query(query)
        print(f"Agent: {response['primary_agent']}")
        print(f"Response: {response['response'][:200]}...")  # Show first 200 chars
        print(f"Next: {response['suggested_next']}")
        print()

def main():
    """Run all demos."""
    print("🚀 Career Mentor Agent Demo")
    print("=" * 60)
    print("This demo shows the core functionality of the Career Mentor Agent")
    print("without requiring the Streamlit interface or Gemini API key.")
    print()
    
    try:
        # Check if Gemini API key is available
        if not config.GEMINI_API_KEY:
            print("⚠️  Warning: GEMINI_API_KEY not found in environment variables")
            print("   Some features may not work without the API key.")
            print("   Set GEMINI_API_KEY in your .env file to enable full functionality.")
            print()
        
        # Run demos
        demo_tools()  # This works without API key
        demo_career_agent()
        demo_skill_agent()
        demo_job_agent()
        demo_orchestrator()
        demo_chat()
        
        print("✅ Demo completed successfully!")
        print("\nTo run the full application:")
        print("1. Set your GEMINI_API_KEY in .env file")
        print("2. Run: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")
        print("This might be due to missing Gemini API key or other configuration issues.")

if __name__ == "__main__":
    main() 