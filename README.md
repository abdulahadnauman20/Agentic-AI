# Student Agent Assistant with Google Gemini

This is a Student Agent Assistant that uses Google's Gemini AI to help students with academic questions, study tips, and text summarization.

## Setup Instructions

### 1. Get Google AI API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root with:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Run the Application

#### Command Line Version:
```bash
python student_agent.py
```

#### Streamlit Web App:
```bash
streamlit run student_agent_app.py
```

## Features

- **Academic Question Answering**: Get help with academic questions
- **Study Tips**: Receive effective study strategies
- **Text Summarization**: Summarize long texts for better understanding

## Requirements

- Python 3.7+
- Google AI API Key
- Internet connection 