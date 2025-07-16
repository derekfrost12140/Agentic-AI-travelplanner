# ✈️ AI Travel Agent

A proof-of-concept AI travel agent built with LangChain and Streamlit that demonstrates agentic AI capabilities. This application showcases how AI agents can use multiple tools to provide comprehensive travel planning assistance.

## 🚀 Features

### Core Capabilities
- **Flight Search**: Find available flights between cities with pricing and timing
- **Hotel Search**: Discover hotels with ratings, amenities, and pricing
- **Weather Information**: Get weather forecasts for travel destinations
- **Travel Recommendations**: Receive personalized recommendations for attractions, restaurants, and activities
- **Interactive Chat Interface**: Natural conversation with the AI agent
- **Itinerary Download**: Download your travel plans in TXT, JSON, or DOCX formats

### Agentic AI Features
- **Multi-Tool Agent**: Uses LangChain's agent framework to coordinate multiple specialized tools
- **Contextual Understanding**: Maintains conversation history for better responses
- **Intelligent Tool Selection**: Automatically chooses the right tools based on user requests
- **Error Handling**: Graceful handling of API errors and edge cases

## 🛠️ Technology Stack

- **LangChain**: Agent framework and tool orchestration
- **OpenAI GPT-3.5-turbo**: Large language model for natural language understanding
- **Streamlit**: Web interface and user experience
- **Python**: Core programming language

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/))

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to your project directory
cd your-project-directory

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
# Copy the example file
cp env_example.txt .env

# Edit the .env file and add your OpenAI API key
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🎯 Usage Examples

### Example 1: Plan a Complete Trip
```
User: "I want to plan a 5-day trip to Paris next month. Can you help me?"

AI Agent: "I'd be happy to help you plan your trip to Paris! To provide the best recommendations, I need a few details:
- What dates are you planning to travel?
- How many people are traveling?
- What's your budget range?
- What are your main interests (culture, food, shopping, etc.)?
- Where will you be departing from?"
```

### Example 2: Flight Search
```
User: "Find flights from New York to Tokyo for next week"

AI Agent: "Found 3 flights from New York to Tokyo on 2024-01-15:

1. Delta Airlines DL123
   Departure: 08:00 | Arrival: 11:30
   Duration: 3h 30m | Price: $450

2. American Airlines AA456
   Departure: 14:15 | Arrival: 17:45
   Duration: 3h 30m | Price: $380

3. United Airlines UA789
   Departure: 20:30 | Arrival: 23:45
   Duration: 3h 15m | Price: $520"
```

### Example 3: Hotel Search
```
User: "Find hotels in Paris for March 15-20"

AI Agent: "Found 3 hotels in Paris from 2024-03-15 to 2024-03-20 (5 nights):

1. Grand Hotel (4.5★)
   Location: City Center
   Price per night: $200
   Total for 5 nights: $1000
   Amenities: WiFi, Pool, Spa, Restaurant

2. Comfort Inn (3.8★)
   Location: Airport Area
   Price per night: $120
   Total for 5 nights: $600
   Amenities: WiFi, Breakfast, Parking

3. Luxury Resort (4.9★)
   Location: Beachfront
   Price per night: $350
   Total for 5 nights: $1750
   Amenities: WiFi, Pool, Spa, Restaurant, Gym, Beach Access"
```

### Example 4: Download Itinerary
After planning your trip, you can download your itinerary in multiple formats:

- **📄 TXT Format**: Simple text file with conversation summary
- **📊 JSON Format**: Structured data for integration with other tools
- **📝 DOCX Format**: Professional Word document with formatting

The download section appears automatically when you have conversation history.

## 🏗️ Architecture

### Core Components

1. **TravelAgent Class** (`travel_agent.py`)
   - Manages the LangChain agent and tools
   - Handles conversation flow and tool execution
   - Provides error handling and response formatting

2. **Tools** (Built-in functions)
   - `search_flights()`: Simulates flight search API
   - `search_hotels()`: Simulates hotel search API
   - `get_weather_forecast()`: Simulates weather API
   - `get_travel_recommendations()`: Provides destination-specific recommendations

3. **Streamlit Interface** (`app.py`)
   - Modern, responsive web UI
   - Real-time chat interface
   - Session state management
   - Quick action buttons

### Agent Flow

```
User Input → LangChain Agent → Tool Selection → Tool Execution → Response Generation → User Output
```

## 🔧 Customization

### Adding New Tools

To add a new tool, modify the `_create_tools()` method in `travel_agent.py`:

```python
@tool
def your_new_tool(param1: str, param2: int) -> str:
    """Description of what your tool does.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
    
    Returns:
        String with tool results
    """
    # Your tool implementation here
    return "Tool results"
```

### Modifying the UI

The Streamlit interface can be customized by:
- Modifying the CSS styles in the `st.markdown()` section
- Adding new sidebar widgets
- Creating additional pages or tabs

## 🧪 Testing

### Manual Testing
1. Start the application
2. Enter your OpenAI API key
3. Try the quick action buttons
4. Test natural language queries
5. Verify tool responses

### Example Test Queries
- "What's the weather in Tokyo tomorrow?"
- "Find hotels in New York for next weekend"
- "Give me recommendations for Paris"
- "Plan a romantic getaway to Venice"

## 📝 Notes

### Current Limitations
- Flight and hotel data are simulated (not real APIs)
- Weather data is mock data
- Limited to predefined cities in recommendations
- No actual booking capabilities

### Future Enhancements
- Integrate real flight/hotel APIs (Skyscanner, Booking.com)
- Add real weather API integration
- Implement booking functionality
- Add more cities and recommendations
- Include image generation for destinations
- Add travel document requirements

## 🤝 Contributing

This is a proof-of-concept project. Feel free to:
- Add new tools and capabilities
- Improve the UI/UX
- Integrate real APIs
- Add more sophisticated agent behaviors

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- LangChain team for the excellent agent framework
- OpenAI for providing the language model capabilities
- Streamlit for the intuitive web framework

---

**Built with Passion by Devansh Swami** 