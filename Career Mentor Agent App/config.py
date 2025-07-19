import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

CAREER_FIELDS = [
    "Software Development", "Data Science", "Cybersecurity", "AI/ML Engineering",
    "Product Management", "UX/UI Design", "Digital Marketing", "Finance",
    "Healthcare", "Education", "Environmental Science", "Creative Arts",
    "Business Administration", "Law", "Engineering", "Sales"
]

SKILL_CATEGORIES = {
    "Technical Skills": ["Programming", "Data Analysis", "System Design", "Cloud Computing"],
    "Soft Skills": ["Communication", "Leadership", "Problem Solving", "Teamwork"],
    "Domain Knowledge": ["Industry Trends", "Business Acumen", "Regulatory Knowledge"],
    "Tools & Technologies": ["Software Tools", "Frameworks", "Platforms", "Methodologies"]
}

AGENT_CONFIGS = {
    "career_agent": {
        "name": "CareerAgent",
        "description": "Specializes in career exploration and path recommendations",
        "model": "gemini-pro"
    },
    "skill_agent": {
        "name": "SkillAgent", 
        "description": "Focuses on skill development and learning roadmaps",
        "model": "gemini-pro"
    },
    "job_agent": {
        "name": "JobAgent",
        "description": "Provides real-world job insights and role information",
        "model": "gemini-pro"
    }
} 