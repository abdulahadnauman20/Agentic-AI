#!/usr/bin/env python3
"""
Simple test to verify Streamlit session state initialization.
"""

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_session_state():
    """Test session state initialization."""
    st.title("Session State Test")
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'interests': [],
            'skills': [],
            'experience_level': 'beginner',
            'goals': []
        }
    
    st.write("Session state initialized successfully!")
    st.write(f"User profile: {st.session_state.user_profile}")
    
    # Test accessing user profile
    interests = st.text_area(
        "Interests",
        value=", ".join(st.session_state.user_profile.get('interests', [])),
        placeholder="Enter your interests"
    )
    
    if st.button("Save"):
        st.session_state.user_profile['interests'] = [i.strip() for i in interests.split(',') if i.strip()]
        st.success("Saved successfully!")
        st.write(f"Updated profile: {st.session_state.user_profile}")

if __name__ == "__main__":
    test_session_state() 