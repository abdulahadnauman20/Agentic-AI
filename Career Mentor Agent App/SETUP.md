# 🚀 Quick Setup Guide

## Career Mentor Agent - Powered by Gemini AI

### Prerequisites
- Python 3.8 or higher
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### 🛠️ Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**
   - Copy `env_template.txt` to `.env`
   - Add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Test the Application**
   ```bash
   python test_app.py
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Open in Browser**
   Navigate to `http://localhost:8501`

### 🎯 What You Can Do

#### Without API Key (Basic Features)
- ✅ View career roadmaps
- ✅ Access job insights
- ✅ Use skill assessment tools
- ✅ Explore the UI

#### With API Key (Full Features)
- 🤖 AI-powered career recommendations
- 🧠 Personalized skill roadmaps
- 💬 Interactive chat with agents
- 📊 Advanced career analysis

### 📁 Project Structure
```
Career Mentor Agent App/
├── app.py                 # Main Streamlit application
├── agents.py              # Multi-agent system (Career, Skill, Job)
├── tools.py               # Career tools and utilities
├── gemini_client.py       # Gemini API client wrapper
├── config.py              # Configuration and constants
├── demo.py                # Demo script for testing
├── test_app.py            # Component testing script
├── requirements.txt       # Python dependencies
├── README.md              # Comprehensive documentation
├── SETUP.md               # This quick setup guide
├── env_template.txt       # Environment variables template
└── .gitignore             # Git ignore rules
```

### 🤖 Multi-Agent System

The application uses three specialized AI agents:

1. **🎯 CareerAgent**: Career exploration and recommendations
2. **📚 SkillAgent**: Learning roadmaps and skill development
3. **💼 JobAgent**: Job market insights and role information

### 🔧 Troubleshooting

#### Common Issues

1. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

2. **API Key Issues**
   - Verify your Gemini API key is correct
   - Check that the `.env` file is in the root directory
   - Ensure the key format is: `GEMINI_API_KEY=your_key_here`

3. **Streamlit Issues**
   - Try running: `streamlit run app.py --server.port 8502`
   - Check if port 8501 is already in use

4. **Session State Errors**
   - Refresh the browser page
   - Clear browser cache
   - Restart the Streamlit app

### 📞 Support

- Check the `README.md` for detailed documentation
- Run `python demo.py` to see examples
- Run `python test_app.py` to verify installation

### 🎉 Ready to Start!

Once you've completed the setup:

1. Open the app in your browser
2. Complete your profile in the Dashboard
3. Explore different career paths
4. Generate personalized skill roadmaps
5. Chat with AI agents for guidance

**Happy career exploring! 🚀** 