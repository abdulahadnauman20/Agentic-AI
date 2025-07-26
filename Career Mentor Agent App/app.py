import streamlit as st
import json
from typing import Dict, List, Any
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from agents import AgentOrchestrator, CareerAgent, SkillAgent, JobAgent
from tools import CareerTools
import config

# Page configuration
st.set_page_config(
    page_title="Career Mentor Agent",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .skill-category {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    
    .roadmap-phase {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables."""
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = AgentOrchestrator()
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'interests': [],
            'skills': [],
            'experience_level': 'beginner',
            'goals': []
        }
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def main():
    # Initialize session state first
    initialize_session_state()
    # Header
    st.markdown("""
    <div class="main-header">
        <h1> Career Mentor Agent</h1>
        <p>Your AI-powered career exploration companion powered by Gemini</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("##  Navigation")
        page = st.selectbox(
            "Choose a section:",
            [" Dashboard", "Career Explorer", "Skill Roadmap", "Job Insights", " Chat with Agents"]
        )
        
        st.markdown("---")
        st.markdown("## Active Agents")
        st.markdown("""
        - **CareerAgent**: Career exploration & recommendations
        - **SkillAgent**: Learning roadmaps & skill development
        - **JobAgent**: Job insights & market analysis
        """)
        
        st.markdown("---")
        st.markdown("##  Settings")
        if st.button("Reset Session"):
            st.session_state.user_profile = {}
            st.session_state.conversation_history = []
            st.rerun()
    
    # Page routing
    if page == " Dashboard":
        show_dashboard()
    elif page == " Career Explorer":
        show_career_explorer()
    elif page == "Skill Roadmap":
        show_skill_roadmap()
    elif page == " Job Insights":
        show_job_insights()
    elif page == " Chat with Agents":
        show_chat_interface()

def show_dashboard():
    """Main dashboard with overview and quick actions."""
    st.markdown("##  Welcome to Your Career Journey")
    
    # Ensure user_profile exists with safe defaults
    user_profile = st.session_state.get('user_profile', {})
    if not user_profile:
        user_profile = {
            'interests': [],
            'skills': [],
            'experience_level': 'beginner',
            'goals': []
        }
        st.session_state.user_profile = user_profile
    
    # User profile section
    with st.expander(" Your Profile", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            interests = st.text_area(
                "What are your interests? (comma-separated)",
                value=", ".join(user_profile.get('interests', [])),
                placeholder="e.g., programming, data analysis, design, business"
            )
            
            experience_level = st.selectbox(
                "Experience Level",
                ["beginner", "intermediate", "advanced"],
                index=["beginner", "intermediate", "advanced"].index(user_profile.get('experience_level', 'beginner'))
            )
        
        with col2:
            skills = st.text_area(
                "Current Skills (comma-separated)",
                value=", ".join(user_profile.get('skills', [])),
                placeholder="e.g., Python, communication, project management"
            )
            
            goals = st.text_area(
                "Career Goals",
                value=", ".join(user_profile.get('goals', [])),
                placeholder="e.g., become a data scientist, start a business"
            )
        
        if st.button("Save Profile"):
            user_profile = {
                'interests': [i.strip() for i in interests.split(',') if i.strip()],
                'skills': [s.strip() for s in skills.split(',') if s.strip()],
                'experience_level': experience_level,
                'goals': [g.strip() for g in goals.split(',') if g.strip()]
            }
            st.session_state.user_profile = user_profile
            st.success("Profile saved successfully!")
    
    # Quick actions
    st.markdown("## Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(" Get Career Recommendations"):
            if st.session_state.user_profile:
                with st.spinner("Analyzing your profile..."):
                    career_agent = CareerAgent()
                    recommendations = career_agent.recommend_careers(
                        st.session_state.user_profile.get('interests', []),
                        st.session_state.user_profile.get('skills', []),
                        st.session_state.user_profile.get('experience_level', 'beginner')
                    )
                    st.session_state.conversation_history.append({
                        'type': 'career_recommendations',
                        'data': recommendations
                    })
                st.rerun()
            else:
                st.warning("Please save your profile first!")
    
    with col2:
        if st.button("Generate Skill Roadmap"):
            career_field = st.selectbox("Select Career Field", config.CAREER_FIELDS)
            if st.button("Generate"):
                with st.spinner("Creating your roadmap..."):
                    skill_agent = SkillAgent()
                    roadmap = skill_agent.generate_skill_roadmap(
                        career_field,
                        st.session_state.user_profile.get('experience_level', 'beginner')
                    )
                    st.session_state.conversation_history.append({
                        'type': 'skill_roadmap',
                        'data': roadmap
                    })
                st.rerun()
    
    with col3:
        if st.button("Get Job Insights"):
            career_field = st.selectbox("Select Field for Insights", config.CAREER_FIELDS)
            if st.button("Get Insights"):
                with st.spinner("Gathering job insights..."):
                    job_agent = JobAgent()
                    insights = job_agent.get_job_insights(career_field)
                    st.session_state.conversation_history.append({
                        'type': 'job_insights',
                        'data': insights
                    })
                st.rerun()
    
    # Recent activity
    if st.session_state.conversation_history:
        st.markdown("##  Recent Activity")
        for i, activity in enumerate(reversed(st.session_state.conversation_history[-5:])):
            with st.expander(f"Activity {len(st.session_state.conversation_history) - i}"):
                if activity['type'] == 'career_recommendations':
                    st.markdown("**Career Recommendations**")
                    st.write(activity['data']['recommendations'])
                elif activity['type'] == 'skill_roadmap':
                    st.markdown("**Skill Roadmap**")
                    st.write(f"Career: {activity['data']['career_field']}")
                    st.write(activity['data']['enhanced_insights'])
                elif activity['type'] == 'job_insights':
                    st.markdown("**Job Insights**")
                    st.write(f"Career: {activity['data']['career_field']}")
                    st.write(activity['data']['market_analysis'])

def show_career_explorer():
    """Career exploration interface."""
    st.markdown("##  Career Explorer")
    
    # Career field selection
    selected_career = st.selectbox(
        "Choose a career field to explore:",
        config.CAREER_FIELDS
    )
    
    if st.button(" Explore Career"):
        with st.spinner("Analyzing career path..."):
            # Get career analysis
            career_agent = CareerAgent()
            analysis = career_agent.analyze_career_fit(
                selected_career,
                st.session_state.user_profile
            )
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("###  Career Analysis")
                st.markdown(f"""
                <div class="agent-card">
                    <h4>{selected_career}</h4>
                    <p>{analysis['analysis']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### Your Profile Match")
                if st.session_state.user_profile:
                    interests = st.session_state.user_profile.get('interests', [])
                    skills = st.session_state.user_profile.get('skills', [])
                    
                    # Create a simple match visualization
                    match_data = {
                        'Category': ['Interests', 'Skills', 'Experience'],
                        'Match Score': [len(interests), len(skills), 1]
                    }
                    df = pd.DataFrame(match_data)
                    
                    fig = px.bar(df, x='Category', y='Match Score', 
                               title="Profile Match Analysis",
                               color='Match Score',
                               color_continuous_scale='viridis')
                    st.plotly_chart(fig, use_container_width=True)
    
    # Career recommendations
    st.markdown("## Recommended Career Paths")
    
    if st.session_state.user_profile:
        with st.spinner("Generating recommendations..."):
            career_agent = CareerAgent()
            recommendations = career_agent.recommend_careers(
                st.session_state.user_profile.get('interests', []),
                st.session_state.user_profile.get('skills', []),
                st.session_state.user_profile.get('experience_level', 'beginner')
            )
            
            st.markdown(recommendations['recommendations'])
    else:
        st.info("Please complete your profile in the Dashboard to get personalized recommendations.")

def show_skill_roadmap():
    """Skill roadmap interface."""
    st.markdown("## Skill Development Roadmap")
    
    # Career field selection
    career_field = st.selectbox(
        "Select your target career field:",
        config.CAREER_FIELDS
    )
    
    experience_level = st.selectbox(
        "Your current experience level:",
        ["beginner", "intermediate", "advanced"]
    )
    
    if st.button(" Generate Roadmap"):
        with st.spinner("Creating your personalized roadmap..."):
            skill_agent = SkillAgent()
            roadmap_data = skill_agent.generate_skill_roadmap(career_field, experience_level)
            
            # Display roadmap
            st.markdown(f"###  {career_field} - {experience_level.title()} Level")
            
            roadmap = roadmap_data['roadmap']['roadmap']
            
            # Create tabs for different phases
            tab1, tab2, tab3 = st.tabs(["Foundation", "Specialization", "Expertise"])
            
            with tab1:
                if 'beginner' in roadmap:
                    phase = roadmap['beginner']
                    st.markdown(f"#### {phase['phase']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Key Skills**")
                        for skill in phase['skills']:
                            st.markdown(f"- {skill}")
                    
                    with col2:
                        st.markdown("* Projects**")
                        for project in phase['projects']:
                            st.markdown(f"- {project}")
                    
                    st.markdown("**📚 Resources**")
                    for resource in phase['resources']:
                        st.markdown(f"- {resource}")
            
            with tab2:
                if 'intermediate' in roadmap:
                    phase = roadmap['intermediate']
                    st.markdown(f"#### {phase['phase']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("** Key Skills**")
                        for skill in phase['skills']:
                            st.markdown(f"- {skill}")
                    
                    with col2:
                        st.markdown("**Projects**")
                        for project in phase['projects']:
                            st.markdown(f"- {project}")
                    
                    st.markdown("**Resources**")
                    for resource in phase['resources']:
                        st.markdown(f"- {resource}")
            
            with tab3:
                if 'advanced' in roadmap:
                    phase = roadmap['advanced']
                    st.markdown(f"#### {phase['phase']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Key Skills**")
                        for skill in phase['skills']:
                            st.markdown(f"- {skill}")
                    
                    with col2:
                        st.markdown("**Projects**")
                        for project in phase['projects']:
                            st.markdown(f"- {project}")
                    
                    st.markdown("**Resources**")
                    for resource in phase['resources']:
                        st.markdown(f"- {resource}")
            
            # Enhanced insights
            st.markdown("###  AI-Enhanced Insights")
            st.markdown(roadmap_data['enhanced_insights'])

def show_job_insights():
    """Job insights interface."""
    st.markdown("## Job Market Insights")
    
    # Career field selection
    career_field = st.selectbox(
        "Select career field for job insights:",
        config.CAREER_FIELDS
    )
    
    if st.button("Get Job Insights"):
        with st.spinner("Gathering job market data..."):
            job_agent = JobAgent()
            insights = job_agent.get_job_insights(career_field)
            
            # Display insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("###  Job Roles")
                
                st.markdown("**Entry Level Roles**")
                for role in insights['job_insights']['entry_level_roles']:
                    st.markdown(f"- {role}")
                
                st.markdown("**Mid Level Roles**")
                for role in insights['job_insights']['mid_level_roles']:
                    st.markdown(f"- {role}")
                
                st.markdown("**Senior Level Roles**")
                for role in insights['job_insights']['senior_level_roles']:
                    st.markdown(f"- {role}")
            
            with col2:
                st.markdown("### Salary Ranges")
                salary_data = insights['job_insights']['salary_ranges']
                
                # Create salary visualization
                salary_df = pd.DataFrame([
                    {'Level': 'Entry', 'Salary': salary_data['entry']},
                    {'Level': 'Mid', 'Salary': salary_data['mid']},
                    {'Level': 'Senior', 'Salary': salary_data['senior']}
                ])
                
                fig = px.bar(salary_df, x='Level', y='Salary', 
                           title="Salary Progression",
                           color='Level',
                           color_discrete_sequence=['#28a745', '#ffc107', '#dc3545'])
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("###  Top Companies")
            for company in insights['job_insights']['companies']:
                st.markdown(f"- {company}")
            
            st.markdown("### Market Analysis")
            st.markdown(insights['market_analysis'])

def show_chat_interface():
    """Chat interface with agents."""
    st.markdown("##  Chat with Career Agents")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about careers, skills, or jobs..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from orchestrator
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.orchestrator.process_user_query(
                    prompt, 
                    st.session_state.user_profile
                )
                
                # Display response
                st.markdown(f"**{response['primary_agent']}**: {response['response']}")
                st.markdown(f"*{response['suggested_next']}*")
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"{response['primary_agent']}: {response['response']}\n\n{response['suggested_next']}"
                })

if __name__ == "__main__":
    main() 
