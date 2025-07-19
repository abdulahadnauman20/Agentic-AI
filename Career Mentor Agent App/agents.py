from typing import Dict, List, Any
from gemini_client import GeminiClient
from tools import CareerTools
import config

class BaseAgent:
    """Base class for all career mentor agents."""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.client = GeminiClient()
        self.config = config.AGENT_CONFIGS.get(agent_type, {})
        self.name = self.config.get("name", "BaseAgent")
        self.description = self.config.get("description", "")
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return f"""You are {self.name}, {self.description}.
        
        You are part of a multi-agent career mentoring system. Your role is to provide 
        expert guidance in your specific domain while working collaboratively with other agents.
        
        Always be helpful, encouraging, and provide actionable advice. Use the available 
        tools when appropriate to provide structured information."""
    
    def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """Process a message and return a response."""
        system_prompt = self.get_system_prompt()
        return self.client.generate_response(message, system_prompt)

class CareerAgent(BaseAgent):
    """Agent specialized in career exploration and path recommendations."""
    
    def __init__(self):
        super().__init__("career_agent")
    
    def get_system_prompt(self) -> str:
        return f"""You are {self.name}, a career exploration specialist. Your expertise includes:

        - Career path analysis and recommendations
        - Industry trends and market insights
        - Personality and interest assessment
        - Career transition guidance
        - Educational pathway recommendations

        You help students and professionals explore different career options based on their 
        interests, skills, and goals. You provide comprehensive career guidance and can 
        recommend specific fields and roles.

        Available career fields: {', '.join(config.CAREER_FIELDS)}

        When recommending careers, consider:
        1. User's interests and passions
        2. Current skills and experience level
        3. Market demand and growth potential
        4. Work-life balance preferences
        5. Geographic and remote work preferences

        Be encouraging and provide actionable next steps."""
    
    def recommend_careers(self, interests: List[str], skills: List[str], 
                         experience_level: str = "beginner") -> Dict[str, Any]:
        """Recommend career paths based on user profile."""
        prompt = f"""
        Based on the following user profile, recommend 3-5 career paths:
        
        Interests: {', '.join(interests)}
        Current Skills: {', '.join(skills)}
        Experience Level: {experience_level}
        
        For each recommended career, provide:
        1. Why it's a good fit
        2. Required skills and qualifications
        3. Growth potential and market demand
        4. Typical career progression
        5. Next steps to get started
        """
        
        response = self.client.generate_structured_response(
            prompt, 
            self.get_system_prompt(),
            "list"
        )
        
        return {
            "agent": self.name,
            "recommendations": response.get("response", "Unable to generate recommendations"),
            "interests_analyzed": interests,
            "skills_considered": skills
        }
    
    def analyze_career_fit(self, career_field: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how well a specific career field fits the user."""
        prompt = f"""
        Analyze the fit between the user and the career field '{career_field}':
        
        User Profile:
        - Interests: {user_profile.get('interests', [])}
        - Skills: {user_profile.get('skills', [])}
        - Experience: {user_profile.get('experience_level', 'beginner')}
        - Goals: {user_profile.get('goals', [])}
        
        Provide:
        1. Fit score (1-10) with explanation
        2. Strengths that align with this career
        3. Potential challenges or gaps
        4. Recommended preparation steps
        5. Alternative career paths to consider
        """
        
        response = self.client.generate_structured_response(
            prompt,
            self.get_system_prompt(),
            "text"
        )
        
        return {
            "agent": self.name,
            "career_field": career_field,
            "analysis": response.get("response", "Unable to analyze career fit"),
            "user_profile": user_profile
        }

class SkillAgent(BaseAgent):
    """Agent focused on skill development and learning roadmaps."""
    
    def __init__(self):
        super().__init__("skill_agent")
    
    def get_system_prompt(self) -> str:
        return f"""You are {self.name}, a skill development specialist. Your expertise includes:

        - Learning roadmap creation
        - Skill gap analysis
        - Educational resource recommendations
        - Project-based learning guidance
        - Certification and training advice

        You help users develop the skills they need for their target careers. You create 
        personalized learning plans and recommend the best resources and projects.

        You have access to detailed career roadmaps and can provide structured learning paths."""
    
    def generate_skill_roadmap(self, career_field: str, experience_level: str = "beginner") -> Dict[str, Any]:
        """Generate a comprehensive skill roadmap for a career field."""
        # Use the CareerTools to get the roadmap
        roadmap = CareerTools.get_career_roadmap(career_field, experience_level)
        
        # Enhance with AI-generated insights
        prompt = f"""
        Enhance this career roadmap for '{career_field}' at '{experience_level}' level:
        
        Current Roadmap: {roadmap}
        
        Provide additional insights on:
        1. Learning priorities and sequence
        2. Time estimates for each skill
        3. Practice exercises and mini-projects
        4. Common pitfalls to avoid
        5. Success metrics and milestones
        6. Alternative learning paths
        """
        
        enhanced_insights = self.client.generate_response(prompt, self.get_system_prompt())
        
        return {
            "agent": self.name,
            "career_field": career_field,
            "experience_level": experience_level,
            "roadmap": roadmap,
            "enhanced_insights": enhanced_insights
        }
    
    def assess_skill_gaps(self, target_skills: List[str], current_skills: List[str]) -> Dict[str, Any]:
        """Assess skill gaps and provide learning recommendations."""
        prompt = f"""
        Analyze the skill gaps between current and target skills:
        
        Target Skills: {', '.join(target_skills)}
        Current Skills: {', '.join(current_skills)}
        
        Provide:
        1. Critical skill gaps (high priority)
        2. Important skill gaps (medium priority)
        3. Nice-to-have skills (low priority)
        4. Learning resources for each gap
        5. Estimated time to acquire each skill
        6. Recommended learning sequence
        7. Practice projects for skill development
        """
        
        response = self.client.generate_structured_response(
            prompt,
            self.get_system_prompt(),
            "list"
        )
        
        return {
            "agent": self.name,
            "skill_gaps": {
                "target_skills": target_skills,
                "current_skills": current_skills,
                "missing_skills": list(set(target_skills) - set(current_skills))
            },
            "analysis": response.get("response", "Unable to assess skill gaps")
        }
    
    def recommend_learning_resources(self, skills: List[str], learning_style: str = "visual") -> Dict[str, Any]:
        """Recommend learning resources for specific skills."""
        prompt = f"""
        Recommend learning resources for the following skills, considering a {learning_style} learning style:
        
        Skills: {', '.join(skills)}
        
        For each skill, provide:
        1. Best online courses (free and paid)
        2. Books and reading materials
        3. Practice platforms and tools
        4. Video tutorials and channels
        5. Community resources and forums
        6. Estimated time commitment
        7. Difficulty level
        """
        
        response = self.client.generate_structured_response(
            prompt,
            self.get_system_prompt(),
            "list"
        )
        
        return {
            "agent": self.name,
            "skills": skills,
            "learning_style": learning_style,
            "recommendations": response.get("response", "Unable to recommend resources")
        }

class JobAgent(BaseAgent):
    """Agent providing real-world job insights and role information."""
    
    def __init__(self):
        super().__init__("job_agent")
    
    def get_system_prompt(self) -> str:
        return f"""You are {self.name}, a job market and career role specialist. Your expertise includes:

        - Job market analysis and trends
        - Role descriptions and responsibilities
        - Salary information and compensation
        - Company insights and culture
        - Interview preparation and job search strategies

        You provide real-world insights about specific job roles, companies, and the job market. 
        You help users understand what different positions entail and how to prepare for them."""
    
    def get_job_insights(self, career_field: str) -> Dict[str, Any]:
        """Get comprehensive job insights for a career field."""
        # Use CareerTools for structured data
        insights = CareerTools.get_job_insights(career_field)
        
        # Enhance with AI-generated insights
        prompt = f"""
        Provide additional job market insights for '{career_field}':
        
        Current Insights: {insights}
        
        Add insights on:
        1. Current market trends and demand
        2. Remote work opportunities
        3. Industry growth projections
        4. Geographic hotspots for this field
        5. Emerging roles and specializations
        6. Required certifications and credentials
        7. Networking strategies for this field
        """
        
        enhanced_insights = self.client.generate_response(prompt, self.get_system_prompt())
        
        return {
            "agent": self.name,
            "career_field": career_field,
            "job_insights": insights,
            "market_analysis": enhanced_insights
        }
    
    def analyze_job_requirements(self, job_title: str, career_field: str) -> Dict[str, Any]:
        """Analyze specific job requirements and qualifications."""
        prompt = f"""
        Provide detailed analysis for the job title '{job_title}' in the field '{career_field}':
        
        Include:
        1. Typical job responsibilities
        2. Required qualifications and experience
        3. Preferred skills and certifications
        4. Salary range and benefits
        5. Work environment and culture
        6. Career progression opportunities
        7. Common interview questions
        8. Application tips and strategies
        """
        
        response = self.client.generate_structured_response(
            prompt,
            self.get_system_prompt(),
            "text"
        )
        
        return {
            "agent": self.name,
            "job_title": job_title,
            "career_field": career_field,
            "analysis": response.get("response", "Unable to analyze job requirements")
        }
    
    def provide_interview_prep(self, job_title: str, career_field: str) -> Dict[str, Any]:
        """Provide interview preparation guidance."""
        prompt = f"""
        Provide comprehensive interview preparation for '{job_title}' in '{career_field}':
        
        Include:
        1. Common technical questions (if applicable)
        2. Behavioral interview questions
        3. Portfolio and project presentation tips
        4. Salary negotiation strategies
        5. Follow-up and thank you notes
        6. Common mistakes to avoid
        7. Questions to ask the interviewer
        8. Dress code and presentation tips
        """
        
        response = self.client.generate_structured_response(
            prompt,
            self.get_system_prompt(),
            "list"
        )
        
        return {
            "agent": self.name,
            "job_title": job_title,
            "career_field": career_field,
            "interview_prep": response.get("response", "Unable to provide interview prep")
        }

class AgentOrchestrator:
    """Orchestrates communication between different agents."""
    
    def __init__(self):
        self.career_agent = CareerAgent()
        self.skill_agent = SkillAgent()
        self.job_agent = JobAgent()
        self.conversation_history = []
    
    def process_user_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user query and route to appropriate agent(s)."""
        # Determine which agent(s) should handle the query
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['career', 'path', 'field', 'recommend']):
            return self._handle_career_query(query, context)
        elif any(word in query_lower for word in ['skill', 'learn', 'roadmap', 'training']):
            return self._handle_skill_query(query, context)
        elif any(word in query_lower for word in ['job', 'role', 'position', 'interview', 'salary']):
            return self._handle_job_query(query, context)
        else:
            # Default to career agent for general queries
            return self._handle_career_query(query, context)
    
    def _handle_career_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle career-related queries."""
        response = self.career_agent.process_message(query, context)
        return {
            "primary_agent": "CareerAgent",
            "response": response,
            "suggested_next": "Would you like to explore skills needed for any specific career?"
        }
    
    def _handle_skill_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle skill-related queries."""
        response = self.skill_agent.process_message(query, context)
        return {
            "primary_agent": "SkillAgent",
            "response": response,
            "suggested_next": "Would you like to learn about job opportunities in this field?"
        }
    
    def _handle_job_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle job-related queries."""
        response = self.job_agent.process_message(query, context)
        return {
            "primary_agent": "JobAgent",
            "response": response,
            "suggested_next": "Would you like to explore the career path for this role?"
        }
    
    def get_comprehensive_guidance(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive guidance from all agents."""
        # Get career recommendations
        career_recs = self.career_agent.recommend_careers(
            user_profile.get('interests', []),
            user_profile.get('skills', []),
            user_profile.get('experience_level', 'beginner')
        )
        
        # Get skill roadmap for top recommendation
        top_career = career_recs.get('recommendations', '').split('\n')[0] if career_recs.get('recommendations') else "Software Development"
        skill_roadmap = self.skill_agent.generate_skill_roadmap(top_career, user_profile.get('experience_level', 'beginner'))
        
        # Get job insights
        job_insights = self.job_agent.get_job_insights(top_career)
        
        return {
            "career_recommendations": career_recs,
            "skill_roadmap": skill_roadmap,
            "job_insights": job_insights,
            "summary": f"Comprehensive guidance for {top_career} career path"
        } 