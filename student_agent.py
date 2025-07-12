import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def answer_academic_question(question):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"You are a helpful academic assistant. Answer this academic question: {question}"
    response = model.generate_content(prompt)
    return response.text.strip()

def provide_study_tips():
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = "You are a helpful academic assistant. Give me 3 effective study tips for students."
    response = model.generate_content(prompt)
    return response.text.strip()

def summarize_text(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"You are a helpful academic assistant. Summarize the following text:\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    print("Welcome to the Smart Student Agent Assistant!")
    print("Options: 1) Academic Question 2) Study Tips 3) Summarize Text")
    choice = input("Choose an option (1/2/3): ")
    if choice == "1":
        question = input("Enter your academic question: ")
        print("\nAnswer:", answer_academic_question(question))
    elif choice == "2":
        print("\nStudy Tips:", provide_study_tips())
    elif choice == "3":
        text = input("Enter text to summarize: ")
        print("\nSummary:", summarize_text(text))
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()