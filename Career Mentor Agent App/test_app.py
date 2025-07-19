#!/usr/bin/env python3
"""
Simple test script to verify the Career Mentor Agent components work correctly.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        import config
        print("✅ config imported successfully")
    except Exception as e:
        print(f"❌ config import failed: {e}")
        return False
    
    try:
        from tools import CareerTools
        print("✅ CareerTools imported successfully")
    except Exception as e:
        print(f"❌ CareerTools import failed: {e}")
        return False
    
    try:
        from gemini_client import GeminiClient
        print("✅ GeminiClient imported successfully")
    except Exception as e:
        print(f"❌ GeminiClient import failed: {e}")
        return False
    
    try:
        from agents import CareerAgent, SkillAgent, JobAgent, AgentOrchestrator
        print("✅ All agents imported successfully")
    except Exception as e:
        print(f"❌ Agents import failed: {e}")
        return False
    
    return True

def test_tools():
    """Test the CareerTools functionality."""
    print("\nTesting CareerTools...")
    
    try:
        from tools import CareerTools
        
        # Test career roadmap
        roadmap = CareerTools.get_career_roadmap("Software Development", "beginner")
        assert roadmap['career_field'] == "Software Development"
        assert roadmap['experience_level'] == "beginner"
        print("✅ Career roadmap generation works")
        
        # Test skill assessment
        assessment = CareerTools.get_skill_assessment(["programming"], ["Python"])
        assert 'recommended_careers' in assessment
        assert 'skill_gaps' in assessment
        print("✅ Skill assessment works")
        
        # Test job insights
        insights = CareerTools.get_job_insights("Data Science")
        assert 'entry_level_roles' in insights
        assert 'salary_ranges' in insights
        print("✅ Job insights work")
        
        return True
        
    except Exception as e:
        print(f"❌ CareerTools test failed: {e}")
        return False

def test_agents_without_api():
    """Test agents without API key (should handle gracefully)."""
    print("\nTesting agents (without API key)...")
    
    try:
        from agents import CareerAgent, SkillAgent, JobAgent
        
        # Test agent initialization
        career_agent = CareerAgent()
        skill_agent = SkillAgent()
        job_agent = JobAgent()
        print("✅ All agents initialized successfully")
        
        # Test that agents handle missing API key gracefully
        try:
            career_agent.recommend_careers(["programming"], ["Python"])
            print("⚠️  Career agent worked without API key (unexpected)")
        except Exception as e:
            if "GEMINI_API_KEY" in str(e):
                print("✅ Career agent properly handles missing API key")
            else:
                print(f"❌ Career agent error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Career Mentor Agent - Component Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test imports
    if test_imports():
        tests_passed += 1
    
    # Test tools
    if test_tools():
        tests_passed += 1
    
    # Test agents
    if test_agents_without_api():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The application is ready to use.")
        print("\nTo run the full application:")
        print("1. Get a Gemini API key from https://makersuite.google.com/app/apikey")
        print("2. Create a .env file with: GEMINI_API_KEY=your_key_here")
        print("3. Run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    main() 