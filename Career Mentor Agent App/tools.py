import json
from typing import Dict, List, Any
import config

class CareerTools:
    """Tools for career exploration and skill roadmap generation."""
    
    @staticmethod
    def get_career_roadmap(career_field: str, experience_level: str = "beginner") -> Dict[str, Any]:
        """
        Generate a comprehensive career roadmap for a specific field.
        
        Args:
            career_field: The career field to generate roadmap for
            experience_level: Current experience level (beginner, intermediate, advanced)
            
        Returns:
            Dictionary containing the career roadmap
        """
        roadmap_templates = {
            "Software Development": {
                "beginner": {
                    "phase": "Foundation (0-6 months)",
                    "skills": [
                        "Programming Fundamentals (Python, JavaScript)",
                        "Version Control (Git)",
                        "Basic Data Structures & Algorithms",
                        "Web Development Basics (HTML, CSS)",
                        "Command Line Interface"
                    ],
                    "projects": [
                        "Personal Portfolio Website",
                        "Simple Calculator App",
                        "Todo List Application"
                    ],
                    "resources": [
                        "freeCodeCamp.org",
                        "The Odin Project",
                        "Harvard CS50"
                    ]
                },
                "intermediate": {
                    "phase": "Specialization (6-18 months)",
                    "skills": [
                        "Advanced Programming Concepts",
                        "Framework Mastery (React, Django, etc.)",
                        "Database Design & Management",
                        "API Development",
                        "Testing & Debugging"
                    ],
                    "projects": [
                        "Full-Stack Web Application",
                        "RESTful API Service",
                        "Database-Driven Application"
                    ],
                    "resources": [
                        "Real-world project experience",
                        "Open source contributions",
                        "Technical blogs and documentation"
                    ]
                },
                "advanced": {
                    "phase": "Expertise (18+ months)",
                    "skills": [
                        "System Design & Architecture",
                        "Cloud Computing (AWS, Azure, GCP)",
                        "DevOps & CI/CD",
                        "Performance Optimization",
                        "Security Best Practices"
                    ],
                    "projects": [
                        "Scalable Microservices Architecture",
                        "Cloud-Native Applications",
                        "Performance-Critical Systems"
                    ],
                    "resources": [
                        "System design interviews",
                        "Advanced certifications",
                        "Industry conferences"
                    ]
                }
            },
            "Data Science": {
                "beginner": {
                    "phase": "Foundation (0-6 months)",
                    "skills": [
                        "Python Programming",
                        "Statistics Fundamentals",
                        "Data Manipulation (Pandas, NumPy)",
                        "Data Visualization (Matplotlib, Seaborn)",
                        "SQL Basics"
                    ],
                    "projects": [
                        "Data Analysis of Public Datasets",
                        "Exploratory Data Analysis",
                        "Simple Predictive Models"
                    ],
                    "resources": [
                        "Kaggle Learn",
                        "DataCamp",
                        "Towards Data Science"
                    ]
                },
                "intermediate": {
                    "phase": "Machine Learning (6-18 months)",
                    "skills": [
                        "Machine Learning Algorithms",
                        "Scikit-learn Framework",
                        "Feature Engineering",
                        "Model Evaluation",
                        "Data Preprocessing"
                    ],
                    "projects": [
                        "Classification/Regression Models",
                        "Natural Language Processing",
                        "Computer Vision Projects"
                    ],
                    "resources": [
                        "Coursera ML Course",
                        "Fast.ai",
                        "Hands-on ML Book"
                    ]
                },
                "advanced": {
                    "phase": "Advanced ML & Production (18+ months)",
                    "skills": [
                        "Deep Learning (TensorFlow, PyTorch)",
                        "MLOps & Model Deployment",
                        "Big Data Technologies",
                        "Advanced Statistics",
                        "Research & Innovation"
                    ],
                    "projects": [
                        "Production ML Systems",
                        "Research Papers Implementation",
                        "Large-Scale Data Processing"
                    ],
                    "resources": [
                        "Research papers",
                        "Advanced courses",
                        "Industry projects"
                    ]
                }
            }
        }
        
        # Get template for the career field, or create a generic one
        if career_field in roadmap_templates:
            roadmap = roadmap_templates[career_field]
        else:
            # Generate a generic roadmap for other fields
            roadmap = {
                "beginner": {
                    "phase": "Foundation (0-6 months)",
                    "skills": [
                        "Industry Fundamentals",
                        "Basic Tools & Software",
                        "Core Concepts",
                        "Entry-level Certifications",
                        "Networking Basics"
                    ],
                    "projects": [
                        "Portfolio Development",
                        "Industry Research",
                        "Skill Demonstration Projects"
                    ],
                    "resources": [
                        "Industry-specific courses",
                        "Professional associations",
                        "Mentorship programs"
                    ]
                },
                "intermediate": {
                    "phase": "Specialization (6-18 months)",
                    "skills": [
                        "Advanced Techniques",
                        "Specialized Tools",
                        "Industry Best Practices",
                        "Leadership Skills",
                        "Project Management"
                    ],
                    "projects": [
                        "Complex Projects",
                        "Team Leadership",
                        "Innovation Initiatives"
                    ],
                    "resources": [
                        "Advanced certifications",
                        "Industry conferences",
                        "Professional development"
                    ]
                },
                "advanced": {
                    "phase": "Expertise (18+ months)",
                    "skills": [
                        "Strategic Thinking",
                        "Industry Innovation",
                        "Thought Leadership",
                        "Advanced Technologies",
                        "Business Acumen"
                    ],
                    "projects": [
                        "Strategic Initiatives",
                        "Industry Publications",
                        "Innovation Leadership"
                    ],
                    "resources": [
                        "Executive education",
                        "Industry leadership",
                        "Research & development"
                    ]
                }
            }
        
        return {
            "career_field": career_field,
            "experience_level": experience_level,
            "roadmap": roadmap,
            "next_steps": [
                "Choose a specific specialization within the field",
                "Set up a learning schedule and milestones",
                "Find mentors or join professional communities",
                "Start working on portfolio projects",
                "Apply for internships or entry-level positions"
            ]
        }
    
    @staticmethod
    def get_job_insights(career_field: str) -> Dict[str, Any]:
        """
        Get real-world job insights for a career field.
        
        Args:
            career_field: The career field to get insights for
            
        Returns:
            Dictionary containing job insights
        """
        job_insights = {
            "Software Development": {
                "entry_level_roles": [
                    "Junior Developer",
                    "Frontend Developer",
                    "Backend Developer",
                    "Full Stack Developer",
                    "QA Engineer"
                ],
                "mid_level_roles": [
                    "Senior Developer",
                    "Team Lead",
                    "Software Architect",
                    "DevOps Engineer",
                    "Technical Lead"
                ],
                "senior_level_roles": [
                    "Principal Engineer",
                    "Engineering Manager",
                    "CTO",
                    "Technical Director",
                    "Software Architect"
                ],
                "salary_ranges": {
                    "entry": "$50,000 - $80,000",
                    "mid": "$80,000 - $130,000",
                    "senior": "$130,000 - $200,000+"
                },
                "companies": [
                    "Google", "Microsoft", "Amazon", "Apple", "Meta",
                    "Netflix", "Uber", "Airbnb", "Stripe", "Shopify"
                ]
            },
            "Data Science": {
                "entry_level_roles": [
                    "Data Analyst",
                    "Junior Data Scientist",
                    "Business Intelligence Analyst",
                    "Data Engineer",
                    "Research Assistant"
                ],
                "mid_level_roles": [
                    "Data Scientist",
                    "Senior Data Analyst",
                    "Machine Learning Engineer",
                    "Data Engineer",
                    "Analytics Manager"
                ],
                "senior_level_roles": [
                    "Senior Data Scientist",
                    "Lead Data Scientist",
                    "Data Science Manager",
                    "Chief Data Officer",
                    "VP of Analytics"
                ],
                "salary_ranges": {
                    "entry": "$60,000 - $90,000",
                    "mid": "$90,000 - $140,000",
                    "senior": "$140,000 - $200,000+"
                },
                "companies": [
                    "Netflix", "Spotify", "Uber", "Airbnb", "Google",
                    "Amazon", "Microsoft", "Meta", "Apple", "LinkedIn"
                ]
            }
        }
        
        # Return specific insights or generic ones
        if career_field in job_insights:
            return job_insights[career_field]
        else:
            return {
                "entry_level_roles": [
                    "Entry-level positions in the field",
                    "Junior roles with training programs",
                    "Assistant positions"
                ],
                "mid_level_roles": [
                    "Specialist positions",
                    "Team lead roles",
                    "Senior positions"
                ],
                "senior_level_roles": [
                    "Manager positions",
                    "Director roles",
                    "Executive positions"
                ],
                "salary_ranges": {
                    "entry": "Varies by industry and location",
                    "mid": "Varies by industry and location",
                    "senior": "Varies by industry and location"
                },
                "companies": [
                    "Industry leaders",
                    "Startups",
                    "Consulting firms",
                    "Government agencies"
                ]
            }
    
    @staticmethod
    def get_skill_assessment(interests: List[str], current_skills: List[str]) -> Dict[str, Any]:
        """
        Assess skills and provide recommendations based on interests.
        
        Args:
            interests: List of user interests
            current_skills: List of current skills
            
        Returns:
            Dictionary containing skill assessment and recommendations
        """
        skill_mapping = {
            "programming": ["Software Development", "Data Science", "AI/ML Engineering"],
            "data": ["Data Science", "Business Intelligence", "Analytics"],
            "design": ["UX/UI Design", "Graphic Design", "Product Design"],
            "business": ["Product Management", "Business Administration", "Consulting"],
            "marketing": ["Digital Marketing", "Content Marketing", "Social Media"],
            "finance": ["Finance", "Investment Banking", "Financial Analysis"],
            "healthcare": ["Healthcare", "Medical Research", "Public Health"],
            "education": ["Education", "Training", "Curriculum Development"]
        }
        
        # Analyze interests and map to potential careers
        recommended_careers = []
        for interest in interests:
            interest_lower = interest.lower()
            for skill, careers in skill_mapping.items():
                if skill in interest_lower:
                    recommended_careers.extend(careers)
        
        # Remove duplicates
        recommended_careers = list(set(recommended_careers))
        
        # Assess skill gaps
        skill_gaps = []
        for career in recommended_careers[:3]:  # Top 3 recommendations
            roadmap = CareerTools.get_career_roadmap(career, "beginner")
            required_skills = roadmap["roadmap"]["beginner"]["skills"]
            
            for skill in required_skills:
                if skill.lower() not in [s.lower() for s in current_skills]:
                    skill_gaps.append(skill)
        
        return {
            "recommended_careers": recommended_careers[:5],
            "skill_gaps": list(set(skill_gaps))[:10],
            "current_skill_level": len(current_skills),
            "recommendations": [
                "Focus on the top 2-3 recommended careers",
                "Start with foundational skills",
                "Build a portfolio of projects",
                "Network with professionals in your target field",
                "Consider internships or entry-level positions"
            ]
        } 