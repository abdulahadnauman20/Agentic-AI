# 💼 Career Mentor Agent
An AI-powered career exploration and guidance application built with **Gemini API** and **Streamlit**. This multi-agent system helps students and professionals explore career paths, develop skills, and understand job market insights.

## 🧠 What It Does

The Career Mentor Agent provides comprehensive career guidance through three specialized AI agents:

- **🎯 CareerAgent**: Recommends career paths based on interests and skills
- **📚 SkillAgent**: Creates personalized learning roadmaps and skill development plans
- **💼 JobAgent**: Provides real-world job insights and market analysis

### Key Features

- **Multi-Agent System**: Seamless handoff between specialized agents
- **Personalized Recommendations**: Based on user interests, skills, and experience level
- **Skill Roadmaps**: Detailed learning paths with projects and resources
- **Job Market Insights**: Salary data, role descriptions, and company information
- **Interactive Chat**: Natural conversation with AI agents
- **Modern UI**: Beautiful, responsive interface built with Streamlit

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Career-Mentor-Agent-App
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
Career Mentor Agent App/
├── app.py                 # Main Streamlit application
├── agents.py              # Multi-agent system implementation
├── tools.py               # Career tools and utilities
├── gemini_client.py       # Gemini API client wrapper
├── config.py              # Configuration and constants
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎯 How to Use

### 1. Dashboard
- Complete your profile with interests, skills, and goals
- Get quick career recommendations
- Access recent activity and insights

### 2. Career Explorer
- Explore specific career fields
- Get detailed career analysis
- View profile match scores

### 3. Skill Roadmap
- Generate personalized learning roadmaps
- View skills needed for different experience levels
- Get project suggestions and learning resources

### 4. Job Insights
- Access job market data and salary information
- View career progression paths
- Get company and role insights

### 5. Chat Interface
- Have natural conversations with AI agents
- Ask specific questions about careers, skills, or jobs
- Get personalized guidance and recommendations

## 🤖 Agent System

### CareerAgent
Specializes in career exploration and recommendations:
- Analyzes user interests and skills
- Recommends suitable career paths
- Provides career fit analysis
- Suggests alternative career options

### SkillAgent
Focuses on skill development and learning:
- Creates comprehensive skill roadmaps
- Identifies skill gaps
- Recommends learning resources
- Suggests practice projects

### JobAgent
Provides job market insights:
- Offers salary information
- Describes job roles and responsibilities
- Provides interview preparation tips
- Shares company and industry insights

## 🛠️ Technical Details

### Technologies Used
- **Streamlit**: Web application framework
- **Google Generative AI**: Gemini API for AI capabilities
- **Plotly**: Data visualization
- **Pandas**: Data manipulation
- **Python-dotenv**: Environment variable management

### Architecture
- **Multi-Agent System**: Three specialized agents with distinct roles
- **Agent Orchestrator**: Routes queries to appropriate agents
- **Tool Integration**: Career roadmap generator and utilities
- **Session Management**: Maintains user state and conversation history

### API Integration
The application uses the **Gemini API** for:
- Natural language processing
- Career recommendations
- Skill analysis
- Job market insights
- Conversational AI

## 📊 Features in Detail

### Career Roadmap Tool
The `get_career_roadmap()` function provides:
- **Phase-based learning**: Beginner, intermediate, and advanced levels
- **Skill progression**: Structured skill development paths
- **Project suggestions**: Hands-on learning opportunities
- **Resource recommendations**: Courses, books, and platforms
- **Time estimates**: Realistic learning timelines

### Multi-Agent Handoff
The system seamlessly switches between agents:
1. **Query Analysis**: Determines the most appropriate agent
2. **Context Sharing**: Passes relevant information between agents
3. **Response Coordination**: Combines insights from multiple agents
4. **Follow-up Suggestions**: Guides users to next steps

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Gemini API key (required)

### Customization
You can customize the application by modifying:
- `config.py`: Career fields, skill categories, and agent configurations
- `tools.py`: Career roadmap templates and job insights data
- `app.py`: UI components and styling

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment
The application can be deployed on:
- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Using the provided requirements.txt
- **AWS/GCP**: Containerized deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google AI**: For providing the Gemini API
- **Streamlit**: For the excellent web framework
- **Open Source Community**: For various Python libraries

## 📞 Support

For questions or support:
- Create an issue in the repository
- Check the documentation
- Review the code comments

---

**Built with ❤️ by Abdul Ahad Nauman using Gemini AI and Streamlit** 