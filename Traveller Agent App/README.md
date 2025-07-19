# 🌍 AI Travel Agent System

A comprehensive travel planning system that uses specialized AI agents with Gemini API to create personalized travel experiences. The system coordinates between multiple agents to handle destination selection, booking, and exploration planning.

## 🚀 Features

### 🤖 Specialized AI Agents
- **DestinationAgent**: Analyzes user preferences and suggests perfect destinations
- **BookingAgent**: Handles flight and hotel bookings with cost optimization
- **ExploreAgent**: Discovers attractions, restaurants, and creates itineraries
- **TravelCoordinator**: Orchestrates the complete workflow between agents

### 🎯 Key Capabilities
- **Mood-based Planning**: Suggests destinations based on travel mood (adventure, relaxation, culture, etc.)
- **Budget Optimization**: Matches recommendations to user budget levels
- **Intelligent Handoffs**: Seamless coordination between specialized agents
- **Mock Data Integration**: Realistic travel data for demonstration
- **Gemini API Integration**: Advanced AI-powered recommendations
- **Session Management**: Track and modify travel plans

### 🛠️ Tools and Handoffs
- **get_flights()**: Search and compare flight options
- **suggest_hotels()**: Find accommodation matching preferences
- **find_attractions()**: Discover points of interest
- **recommend_restaurants()**: Suggest dining experiences
- **plan_itinerary()**: Create day-by-day travel plans

## 📋 Requirements

- Python 3.8+
- Google Generative AI (Gemini) API key
- Internet connection for API calls

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd Traveller-Agent-App
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up Gemini API key**:
```bash
# On Windows
set GEMINI_API_KEY=your_api_key_here

# On macOS/Linux
export GEMINI_API_KEY=your_api_key_here
```

4. **Get your Gemini API key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy and set it as an environment variable

## 🚀 Usage

### Running the Application

```bash
python main.py
```

### Interactive Menu Options

1. **🎯 Create New Travel Plan**: Start a complete travel planning session
2. **📊 View Session Status**: Check the progress of your planning session
3. **✏️ Modify Existing Plan**: Update preferences and requirements
4. **📈 System Statistics**: View system performance and agent information
5. **🧪 Demo Individual Agents**: Test specific agents independently
6. **🚪 Exit**: Close the application

### Example Usage Flow

1. **Start Planning**:
   ```
   Choose option 1: Create New Travel Plan
   ```

2. **Enter Preferences**:
   ```
   Name: John Doe
   Mood: 3 (Culture)
   Budget: 2 (Moderate)
   Destinations: Paris, Rome
   Special Requirements: wheelchair accessible
   ```

3. **Review Results**:
   The system will provide:
   - Destination recommendations with match scores
   - Flight options with pricing
   - Hotel suggestions with amenities
   - Attraction and restaurant recommendations
   - Complete day-by-day itinerary

## 🏗️ System Architecture

### Agent Hierarchy
```
TravelCoordinator (Main Orchestrator)
├── DestinationAgent (Destination Selection)
├── BookingAgent (Flights & Hotels)
└── ExploreAgent (Attractions & Activities)
```

### Data Flow
1. **User Input** → TravelCoordinator
2. **Destination Planning** → DestinationAgent
3. **Booking Planning** → BookingAgent
4. **Exploration Planning** → ExploreAgent
5. **Plan Assembly** → TravelCoordinator
6. **Final Output** → Complete Travel Plan

### Key Components

#### `models.py`
- Data structures for travel requests, destinations, flights, hotels, etc.
- Enums for travel moods and budget levels
- Standardized response formats

#### `base_agent.py`
- Abstract base class for all agents
- Common functionality for Gemini API integration
- Tool management and conversation history

#### `mock_data.py`
- Realistic mock data generators
- Flight, hotel, attraction, and restaurant data
- Configurable data sources

#### `travel_coordinator.py`
- Main orchestrator for the planning workflow
- Handles agent handoffs and session management
- Creates complete travel plans

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `GEMINI_MODEL`: Model to use (default: "gemini-1.5-flash")

### Configuration Options
```python
# In config.py
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30
MOCK_FLIGHTS_ENABLED = True
MOCK_HOTELS_ENABLED = True
MOCK_ATTRACTIONS_ENABLED = True
```

## 🧪 Testing Individual Agents

### DestinationAgent Demo
```python
from destination_agent import DestinationAgent
from models import TravelRequest, TravelMood, BudgetLevel

agent = DestinationAgent()
request = TravelRequest(
    user_name="Test User",
    mood=TravelMood.ADVENTURE,
    budget=BudgetLevel.MODERATE
)
response = await agent.process_request(request)
```

### BookingAgent Demo
```python
from booking_agent import BookingAgent

agent = BookingAgent()
request = {
    "travel_request": travel_request,
    "destination": selected_destination
}
response = await agent.process_request(request)
```

### ExploreAgent Demo
```python
from explore_agent import ExploreAgent

agent = ExploreAgent()
request = {
    "travel_request": travel_request,
    "destination": selected_destination
}
response = await agent.process_request(request)
```

## 📊 Mock Data Features

### Available Destinations
- Bali, Indonesia (Relaxation, Culture, Beach)
- Tokyo, Japan (Urban, Culture, Food)
- Paris, France (Culture, Food, Urban)
- New York, USA (Urban, Culture, Food)
- Swiss Alps, Switzerland (Adventure, Mountains, Nature)

### Data Generation
- **Flights**: Realistic airline names, routes, pricing
- **Hotels**: Chain hotels with amenities and ratings
- **Attractions**: Museums, parks, historical sites
- **Restaurants**: Various cuisines with ratings and specialties

## 🔄 Agent Handoffs

### Handoff Process
1. **Context Preservation**: Each agent maintains conversation history
2. **Data Transfer**: Structured data passed between agents
3. **Error Handling**: Graceful fallbacks if agents fail
4. **Session Tracking**: Complete audit trail of planning process

### Handoff Examples
```python
# DestinationAgent → BookingAgent
destination = destination_response.data["recommendations"][0]["destination"]
booking_request = {
    "travel_request": request,
    "destination": destination
}

# BookingAgent → ExploreAgent
explore_request = {
    "travel_request": request,
    "destination": destination
}
```

## 🎨 Customization

### Adding New Agents
1. Inherit from `BaseAgent`
2. Implement `process_request()` method
3. Add to `TravelCoordinator`
4. Update handoff logic

### Extending Mock Data
1. Add new data sources to `MockDataGenerator`
2. Update data structures in `models.py`
3. Modify agent logic to use new data

### Custom Tools
```python
def add_custom_tool(self):
    self.add_tool({
        "name": "custom_function",
        "description": "Description of the tool",
        "parameters": {
            "param1": "Parameter description"
        }
    })
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Found**:
   ```
   Warning: GEMINI_API_KEY not found in environment variables
   ```
   - Set the environment variable correctly
   - Restart your terminal/IDE

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'google.generativeai'
   ```
   - Install requirements: `pip install -r requirements.txt`

3. **Mock Mode**:
   - System runs in demo mode without API key
   - All functionality works with mock data
   - Set API key for full AI capabilities

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance

### Optimization Features
- **Async Processing**: Non-blocking agent operations
- **Caching**: Conversation history and session data
- **Error Recovery**: Graceful handling of API failures
- **Resource Management**: Efficient memory usage

### Scalability
- **Modular Design**: Easy to add new agents
- **Stateless Operations**: Session-based state management
- **API Rate Limiting**: Built-in request throttling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- OpenAI Agent SDK concepts for inspiration
- Travel industry data patterns for mock data

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

---

**Happy Travel Planning! 🌍✈️🏖️** 