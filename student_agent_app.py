import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

st.title("Student Agent Assistant")

option = st.selectbox(
    "What would you like to do?",
    ("Answer Academic Question", "Get Study Tips", "Summarize Text")
)

if option == "Answer Academic Question":
    question = st.text_input("Enter your academic question:")
    if st.button("Get Answer") and question:
        messages = [
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": f"Answer this academic question: {question}"}
        ]
        answer = get_openai_response(messages)
        st.success(answer)

elif option == "Get Study Tips":
    if st.button("Show Study Tips"):
        messages = [
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": "Give me 3 effective study tips for students."}
        ]
        tips = get_openai_response(messages)
        st.info(tips)

elif option == "Summarize Text":
    text = st.text_area("Enter text to summarize:")
    if st.button("Summarize") and text:
        messages = [
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": f"Summarize the following text:\n{text}"}
        ]
        summary = get_openai_response(messages)
        st.success(summary)