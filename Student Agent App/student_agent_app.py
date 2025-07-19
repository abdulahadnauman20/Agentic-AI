import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

st.title("Student Agent Assistant")

option = st.selectbox(
    "What would you like to do?",
    ("Answer Academic Question", "Get Study Tips", "Summarize Text")
)

if option == "Answer Academic Question":
    question = st.text_input("Enter your academic question:")
    if st.button("Get Answer") and question:
        prompt = f"You are a helpful academic assistant. Answer this academic question: {question}"
        answer = get_gemini_response(prompt)
        st.success(answer)

elif option == "Get Study Tips":
    if st.button("Show Study Tips"):
        prompt = "You are a helpful academic assistant. Give me 3 effective study tips for students."
        tips = get_gemini_response(prompt)
        st.info(tips)

elif option == "Summarize Text":
    text = st.text_area("Enter text to summarize:")
    if st.button("Summarize") and text:
        prompt = f"You are a helpful academic assistant. Summarize the following text:\n{text}"
        summary = get_gemini_response(prompt)
        st.success(summary)