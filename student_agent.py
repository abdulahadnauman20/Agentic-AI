import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def answer_academic_question(question):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": f"Answer this academic question: {question}"}
        ]
    )
    return response.choices[0].message.content.strip()

def provide_study_tips():
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": "Give me 3 effective study tips for students."}
        ]
    )
    return response.choices[0].message.content.strip()

def summarize_text(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": f"Summarize the following text:\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

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