# ✈️ AI Travel Agent

A comprehensive AI travel planner built with LangChain and Streamlit that integrates real APIs for flights, hotels, weather, and travel recommendations. This application demonstrates advanced agentic AI capabilities with real-time data integration and intelligent fallback systems.

## 🚀 Features

### Core Capabilities
- **Real Flight Search**: Integration with Amadeus API for actual flight data with multi-segment routes
- **Enhanced Hotel Search**: Real hotel data from Amadeus API with city-specific fallbacks
- **Live Weather Information**: OpenWeatherMap API integration with Fahrenheit temperature display
- **Travel Recommendations**: Personalized recommendations for attractions, restaurants, and activities
- **Interactive Chat Interface**: Natural conversation with context-aware AI agent
- **Itinerary Download**: Download your travel plans in TXT, JSON, or DOCX formats
- **Cultural Insights**: Destination-specific cultural recommendations and travel tips

### Advanced AI Features
- **Multi-Tool Agent**: Uses LangChain's agent framework to coordinate multiple specialized tools
- **Contextual Understanding**: Maintains conversation history for better responses
- **Intelligent Tool Selection**: Automatically chooses the right tools based on user requests
- **Robust Error Handling**: Graceful handling of API errors with intelligent fallback systems
- **Date Validation**: Smart date handling for past/future travel planning
- **Temperature Unit Preferences**: Automatic Fahrenheit display for US users

### Real API Integrations
- **Amadeus Flight Search**: Real flight offers with pricing, routes, and availability
- **Amadeus Hotel Reference Data**: Actual hotel listings with location and chain information
- **OpenWeatherMap**: Live weather forecasts with proper date validation
- **City Code Resolution**: Intelligent city name to IATA code conversion

## 🤖 Agentic AI Implementation

This project demonstrates the power of **Agentic AI** in real-world applications through a sophisticated travel planning system. The AI agent operates as an autonomous travel consultant that can:

- **Multi-Tool Orchestration**: Seamlessly coordinates between flight search, hotel booking, weather forecasting, and travel recommendations
- **Intelligent Decision Making**: Automatically selects the best API endpoints, handles errors gracefully, and provides fallback options
- **Contextual Understanding**: Maintains conversation context across multiple user interactions and remembers preferences
- **Proactive Problem Solving**: Identifies potential issues (like past dates, API failures) and suggests alternatives
- **Natural Language Processing**: Understands complex travel requests in natural language and breaks them down into actionable tasks

**What This Project Proves:**
This travel planner showcases how agentic AI can transform complex, multi-step processes into seamless user experiences. It proves that AI agents can handle real-world scenarios involving multiple external APIs, error handling, and user preferences while maintaining conversational flow. The system demonstrates that agentic AI is not just about individual tools, but about creating intelligent workflows that adapt to user needs, handle failures gracefully, and provide comprehensive solutions. This approach can be applied to any domain requiring coordination between multiple services, making it a powerful paradigm for building next-generation AI applications.

## 🛠️ Technology Stack

- **LangChain**: Agent framework and tool orchestration
- **OpenAI GPT-3.5-turbo**: Large language model for natural language understanding
- **Streamlit**: Modern web interface with responsive design
- **Amadeus API**: Real flight and hotel data
- **OpenWeatherMap API**: Live weather information
- **Python**: Core programming language with async capabilities

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/))
- Amadeus API credentials (get from [Amadeus for Developers](https://developers.amadeus.com/))
- OpenWeatherMap API key (get from [OpenWeatherMap](https://openweathermap.org/api))

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to your project directory
cd your-project-directory

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
# Copy the example file
cp env_example.txt .env

# Edit the .env file and add your API keys
OPENAI_API_KEY=your_actual_openai_api_key_here
AMADEUS_CLIENT_ID=your_amadeus_client_id_here
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🎯 Usage Examples

### Example 1: Real Flight Search
```
User: "Find flights from New York to Tokyo for August 20-September 3, 2025"

AI Agent: "Found 5 round-trip flight offers from JFK to HND (currency: USD):

1. Outbound: JFK → HNL (AS 8051, Aug 20) → HNL → HND (AS 8457, Aug 20)
   Return: HND → HNL (AS 8458, Sep 03) → HNL → JFK (AS 8050, Sep 03)
   Total Price: 2550.82 USD

2. Outbound: JFK → ICN (OZ 221, Aug 20) → ICN → HND (OZ 178, Aug 21)
   Return: HND → ICN (OZ 177, Sep 03) → ICN → JFK (OZ 224, Sep 03)
   Total Price: 2939.22 USD"
```

### Example 2: Real Hotel Search
```
User: "Find hotels in Dallas for August 10-20, 2025"

AI Agent: "Found 36 hotels in Dallas from 2025-08-10 to 2025-08-20 (10 nights) [Amadeus API]:

1. THE JOULE PREFERRED HOTEL
   Chain: PH | IATA: DAL
   Location: Dallas, US
   Distance: 0.37 KM from city center
   Estimated Price: $200 per night
   Total for 10 nights: $2000
   Coordinates: 32.7807, -96.79843

2. ADOLPHUS
   Chain: WW | IATA: DFW
   Location: Dallas, US
   Distance: 0.43 KM from city center
   Estimated Price: $200 per night
   Total for 10 nights: $2000"
```

### Example 3: Live Weather Information
```
User: "What's the weather in Tokyo on August 20, 2025?"

AI Agent: "Weather forecast for Tokyo on 2025-07-21 18:00:00: 79.68°F, broken clouds"
```

### Example 4: Cultural Recommendations
```
User: "Give me cultural recommendations for Tokyo"

AI Agent: "Travel recommendations for Tokyo:

Top Attractions:
1. Senso-ji Temple
2. Tokyo Skytree
3. Shibuya Crossing
4. Tsukiji Fish Market

Recommended Restaurants:
1. Sukiyabashi Jiro
2. Narisawa
3. Den

Popular Activities:
1. Cherry Blossom Viewing
2. Robot Restaurant Show
3. Traditional Tea Ceremony

Travel Tips:
1. Get a Japan Rail Pass for train travel
2. Learn basic Japanese phrases"
```

## 🏗️ Architecture

### Core Components

1. **TravelAgent Class** (`travel_agent.py`)
   - Manages the LangChain agent and tools
   - Handles conversation flow and tool execution
   - Provides robust error handling and intelligent fallbacks
   - Coordinates multiple API integrations

2. **Real API Tools**
   - `search_flights_amadeus()`: Real flight search with Amadeus API
   - `search_hotels_amadeus()`: Real hotel data with reference API
   - `get_weather_forecast()`: Live weather with OpenWeatherMap API
   - `get_travel_recommendations()`: Curated destination recommendations

3. **Enhanced Streamlit Interface** (`app.py`)
   - Modern, responsive web UI with improved styling
   - Real-time chat interface with message history
   - Session state management with conversation persistence
   - Quick action buttons for common queries
   - Download functionality for itineraries

### API Integration Flow

```
User Input → LangChain Agent → Tool Selection → API Call → Response Processing → Fallback System → User Output
```

### Fallback System

The application features a sophisticated fallback system:

1. **Primary**: Real API data (Amadeus, OpenWeatherMap)
2. **Secondary**: City-specific curated data for major destinations
3. **Tertiary**: Generic simulated data for unsupported locations

## 🔧 Customization

### Adding New APIs

To add a new API integration, modify the `_create_tools()` method in `travel_agent.py`:

```python
@tool
def your_new_api_tool(param1: str, param2: int) -> str:
    """Description of what your tool does.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
    
    Returns:
        String with API results
    """
    # Your API implementation here
    return "API results"
```

### Modifying Fallback Data

City-specific fallback data can be customized in the hotel search function:

```python
# Add new city-specific hotels
elif 'your_city' in city_lower:
    hotels = [
        {"name": "Hotel Name", "rating": 4.5, "location": "Area", "price": 200, "amenities": ["WiFi", "Pool"]}
    ]
```

## 🧪 Testing

### Manual Testing
1. Start the application with all API keys configured
2. Test real flight searches with future dates
3. Verify hotel data from Amadeus API
4. Check weather forecasts for various cities
5. Test fallback systems with unsupported locations

### Example Test Queries
- "Find flights from DFW to DEL for August 10-20, 2025"
- "Show me hotels in Dallas for next month"
- "What's the weather in New York today?"
- "Give me cultural recommendations for Paris"
- "Plan a complete trip to Tokyo for September"

## 📝 Recent Improvements

### API Integrations
- ✅ **Real Flight Data**: Amadeus API integration with multi-segment routes
- ✅ **Live Hotel Data**: Amadeus Hotel Reference API with city codes
- ✅ **Live Weather**: OpenWeatherMap API with proper date validation
- ✅ **Temperature Units**: Automatic Fahrenheit display for US users

### Enhanced Features
- ✅ **City Code Resolution**: Intelligent city name to IATA code conversion
- ✅ **Date Validation**: Smart handling of past/future dates
- ✅ **Fallback Systems**: Graceful degradation when APIs fail
- ✅ **Cultural Recommendations**: Destination-specific insights and tips
- ✅ **Improved UI**: Better styling and user experience

### Error Handling
- ✅ **API Error Recovery**: Intelligent fallback to curated data
- ✅ **Date Validation**: Prevents searches for past dates
- ✅ **City Resolution**: Handles various city name formats
- ✅ **Temperature Conversion**: Proper unit handling

## 🔮 Future Enhancements

### Planned Features
- **Booking Integration**: Direct booking capabilities
- **More APIs**: Additional hotel and flight providers
- **Image Generation**: AI-generated destination images
- **Travel Documents**: Visa and document requirements
- **Multi-language Support**: International language support
- **Mobile App**: Native mobile application

### Technical Improvements
- **Caching**: API response caching for better performance
- **Rate Limiting**: Intelligent API rate limit management
- **Analytics**: User behavior and usage analytics
- **A/B Testing**: Interface and feature testing

## 🤝 Contributing

This project welcomes contributions! Areas for improvement:
- Add new API integrations
- Improve the UI/UX design
- Enhance the fallback systems
- Add more sophisticated agent behaviors
- Implement new features and capabilities

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- **LangChain team** for the excellent agent framework
- **OpenAI** for providing the language model capabilities
- **Amadeus** for flight and hotel data APIs
- **OpenWeatherMap** for weather data
- **Streamlit** for the intuitive web framework

---

**Built with Passion by Devansh Swami** 

*Last Updated: July 2025* 