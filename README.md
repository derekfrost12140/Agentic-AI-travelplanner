# ✈️ AI Travel Agent

A comprehensive AI travel planner built with LangChain and Streamlit that integrates real APIs for flights, hotels, weather, and travel recommendations. This application demonstrates advanced agentic AI capabilities with real-time data integration, intelligent fallback systems, and complete booking functionality.

## 🚀 Features

### Core Capabilities
- **Real Flight Search & Booking**: Integration with Amadeus API for actual flight data with multi-segment routes and complete booking workflow
- **Enhanced Hotel Search & Booking**: Real hotel data from Amadeus API with city-specific fallbacks and booking confirmation
- **Live Weather Information**: OpenWeatherMap API integration with Fahrenheit temperature display
- **Travel Recommendations**: Personalized recommendations for attractions, restaurants, and activities with improved formatting
- **Interactive Chat Interface**: Natural conversation with context-aware AI agent
- **Complete Booking System**: Flight and hotel booking with confirmation emails and reference numbers
- **Beautiful Trip Summaries**: Comprehensive trip overviews with proper formatting and emojis
- **Itinerary Download**: Download your travel plans in TXT, JSON, or DOCX formats
- **Cultural Insights**: Destination-specific cultural recommendations and travel tips

### Advanced AI Features
- **Multi-Tool Agent**: Uses LangChain's agent framework to coordinate multiple specialized tools
- **Contextual Understanding**: Maintains conversation history for better responses
- **Intelligent Tool Selection**: Automatically chooses the right tools based on user requests
- **Robust Error Handling**: Graceful handling of API errors with intelligent fallback systems
- **Date Validation**: Smart date handling for past/future travel planning
- **Temperature Unit Preferences**: Automatic Fahrenheit display for US users
- **Flight Booking Workflow**: Complete booking process with confirmation and next steps
- **Hotel Booking Workflow**: Hotel selection and booking with detailed confirmation

### Real API Integrations
- **Amadeus Flight Search**: Real flight offers with pricing, routes, and availability
- **Amadeus Hotel Reference Data**: Actual hotel listings with location and chain information
- **OpenWeatherMap**: Live weather forecasts with proper date validation
- **City Code Resolution**: Intelligent city name to IATA code conversion
- **DuckDuckGo API**: Real-time web search for travel recommendations (free, no API key needed)

## 🤖 Agentic AI Implementation

This project demonstrates the power of **Agentic AI** in real-world applications through a sophisticated travel planning system. The AI agent operates as an autonomous travel consultant that can:

- **Multi-Tool Orchestration**: Seamlessly coordinates between flight search, hotel booking, weather forecasting, and travel recommendations
- **Intelligent Decision Making**: Automatically selects the best API endpoints, handles errors gracefully, and provides fallback options
- **Contextual Understanding**: Maintains conversation context across multiple user interactions and remembers preferences
- **Proactive Problem Solving**: Identifies potential issues (like past dates, API failures) and suggests alternatives
- **Natural Language Processing**: Understands complex travel requests in natural language and breaks them down into actionable tasks
- **Complete Booking Workflows**: Handles entire booking processes from search to confirmation
- **Smart Response Formatting**: Automatically formats responses for optimal readability and user experience

**What This Project Proves:**
This travel planner showcases how agentic AI can transform complex, multi-step processes into seamless user experiences. It proves that AI agents can handle real-world scenarios involving multiple external APIs, error handling, user preferences, and complete booking workflows while maintaining conversational flow. The system demonstrates that agentic AI is not just about individual tools, but about creating intelligent workflows that adapt to user needs, handle failures gracefully, and provide comprehensive solutions. This approach can be applied to any domain requiring coordination between multiple services, making it a powerful paradigm for building next-generation AI applications.

## 🛠️ Technology Stack

- **LangChain**: Agent framework and tool orchestration
- **OpenAI GPT-3.5-turbo**: Large language model for natural language understanding
- **Streamlit**: Modern web interface with responsive design
- **Amadeus API**: Real flight and hotel data
- **OpenWeatherMap API**: Live weather information
- **DuckDuckGo API**: Free web search for travel recommendations
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

### Example 1: Complete Flight Search & Booking
```
User: "Find flights from New York to Tokyo for August 20-September 3, 2025"

AI Agent: "Found 5 round-trip flight offers from JFK to HND (currency: USD):

**Option 1: Turkish Airlines**
**Total Price: 1357.21 USD**
**Outbound Flight:**
• JFK → IST (Turkish Airlines 192, Aug 20)
• IST → HND (Turkish Airlines 198, Aug 21)
**Return Flight:**
• HND → IST (Turkish Airlines 199, Sep 03)
• IST → JFK (Turkish Airlines 191, Sep 04)

Please select a flight option by responding with the option number (1, 2, 3, etc.) to proceed with booking."

User: "1"

AI Agent: "**🎉 Flight Booking Confirmed!**
**Booking Reference:** BK20250717003143
**Route:** JFK → HND → JFK
**Travel Dates:** 2025-08-20 to 2025-09-03
**Selected Option:** 1

**Booking Details:**
• Your flight has been successfully booked
• You will receive a confirmation email shortly
• Please arrive at the airport 2 hours before departure for international flights
• Don't forget to bring your passport and travel documents

**Next Steps:**
• Check your email for detailed itinerary
• Download your boarding pass 24 hours before departure
• Consider booking hotels and activities for your trip

Thank you for choosing our AI Travel Agent! ✈️"
```

### Example 2: Complete Hotel Search & Booking
```
User: "Find hotels in Tokyo for August 22-25, 2025"

AI Agent: "Found 6 hotels in Tokyo from 2025-08-22 to 2025-08-25 (3 nights) [Local Recommendations]:

1. **Park Hyatt Tokyo (4.8★)**
   - **Location:** Shinjuku
   - **Price per Night:** $450
   - **Total for 3 Nights:** $1350
   - **Amenities:** WiFi, Pool, Spa, Restaurant, City View

2. **Aman Tokyo (4.9★)**
   - **Location:** Otemachi
   - **Price per Night:** $800
   - **Total for 3 Nights:** $2400
   - **Amenities:** WiFi, Spa, Restaurant, Gym, Concierge

Please select a hotel option by responding with the option number (1, 2, 3, etc.) to proceed with booking."

User: "1"

AI Agent: "**🏨 Hotel Booking Confirmed!**
**Booking Reference:** HT20250717004132
**Hotel Location:** Tokyo
**Check-in:** 2025-08-22
**Check-out:** 2025-08-25
**Selected Option:** 1

**Booking Details:**
• Your hotel has been successfully booked
• You will receive a confirmation email shortly
• Check-in time is typically 3:00 PM
• Check-out time is typically 11:00 AM

**Next Steps:**
• Check your email for detailed reservation
• Contact the hotel directly for early check-in requests
• Consider booking airport transfers

Thank you for choosing our AI Travel Agent! 🏨"
```

### Example 3: Live Weather Information
```
User: "What's the weather in Tokyo on August 20, 2025?"

AI Agent: "Weather forecast for Tokyo on 2025-08-20: 79.68°F, broken clouds"
```

### Example 4: Beautiful Travel Recommendations
```
User: "Give me travel recommendations for Tokyo"

AI Agent: "Here are some recommendations for activities in Tokyo:

**Top Attractions:**
• Senso-ji Temple
• Tokyo Skytree
• Shibuya Crossing
• Tsukiji Fish Market

**Recommended Restaurants:**
• Sukiyabashi Jiro
• Narisawa
• Den

**Popular Activities:**
• Cherry Blossom Viewing
• Robot Restaurant Show
• Traditional Tea Ceremony

**Travel Tips:**
• Get a Japan Rail Pass for train travel
• Learn basic Japanese phrases

These activities and attractions will give you a fantastic experience in Tokyo! 🇯🇵"
```

### Example 5: Comprehensive Trip Summary
```
User: "Give me a summary of my trip"

AI Agent: "**✈️ TRIP SUMMARY**

**Destination:** Tokyo, Japan
**Travel Dates:** August 20, 2025 - September 3, 2025
**Number of Travelers:** 1

**🛫 FLIGHT DETAILS**
• **Airline:** Turkish Airlines
• **Route:** JFK → IST (TK 192, Aug 20) → IST → HND (TK 198, Aug 21) → HND → IST (TK 199, Sep 03) → IST → JFK (TK 191, Sep 04)
• **Total Flight Cost:** $1357.21 USD

**🏨 HOTEL DETAILS**
• **Hotel Name:** Park Hyatt Tokyo
• **Location:** Shinjuku, Tokyo
• **Price per Night:** $450
• **Total Hotel Cost:** $1350 for 3 nights
• **Amenities:** WiFi, Pool, Spa, Restaurant, City View

**💰 TOTAL TRIP COST**
• **Flight:** $1357.21 USD
• **Hotel:** $1350 USD
• **Total Trip Cost:** $2707.21 USD

**🎯 TRAVEL RECOMMENDATIONS**
**Top Attractions:**
• Senso-ji Temple
• Tokyo Skytree
• Shibuya Crossing
• Tsukiji Fish Market

**📋 IMPORTANT REMINDERS**
• Check your email for detailed itinerary
• Download boarding pass 24 hours before departure
• Arrive at the airport 2 hours before international flights
• Don't forget your passport and travel documents

Have an amazing trip to Tokyo! 🗼🇯🇵"
```

## 🏗️ Architecture

### Core Components

1. **TravelAgent Class** (`travel_agent.py`)
   - Manages the LangChain agent and tools
   - Handles conversation flow and tool execution
   - Provides robust error handling and intelligent fallbacks
   - Coordinates multiple API integrations
   - Implements complete booking workflows

2. **Real API Tools**
   - `search_flights_amadeus()`: Real flight search with Amadeus API
   - `book_flight()`: Complete flight booking with confirmation
   - `search_hotels_amadeus()`: Real hotel data with reference API
   - `book_hotel()`: Complete hotel booking with confirmation
   - `get_weather_forecast()`: Live weather with OpenWeatherMap API
   - `get_travel_recommendations()`: Curated destination recommendations with web search fallback

3. **Enhanced Streamlit Interface** (`app.py`)
   - Modern, responsive web UI with improved styling
   - Real-time chat interface with message history
   - Session state management with conversation persistence
   - Quick action buttons for common queries
   - Download functionality for itineraries
   - Better error handling and response validation

### API Integration Flow

```
User Input → LangChain Agent → Tool Selection → API Call → Response Processing → Fallback System → Beautiful Formatting → User Output
```

### Multi-Tier Fallback System

The application features a sophisticated multi-tier fallback system:

1. **Primary**: Real API data (Amadeus, OpenWeatherMap, DuckDuckGo)
2. **Secondary**: City-specific curated data for major destinations
3. **Tertiary**: Generic simulated data for unsupported locations

### Flight Search & Booking Flow
```
Flight Search Request → Amadeus API → Format Results → Show Options → User Selection → Booking Confirmation → Reference Number
```

### Hotel Search & Booking Flow
```
Hotel Search Request → Amadeus API → Format Results → Show Options → User Selection → Booking Confirmation → Reference Number
```

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

### Adding New Airlines

To add new airline codes, update the `airline_names` dictionary in the flight search function:

```python
airline_names = {
    # Existing airlines...
    'NEW': 'New Airline Name',
    'ABC': 'Another Airline Company'
}
```

## 🧪 Testing

### Complete Testing Guide

Test all functionality with these prompts:

1. **Flight Search & Booking:**
   ```
   Find flights from DFW to HND for August 10-20, 2025
   ```
   Then respond with: `1` (to test booking)

2. **Hotel Search & Booking:**
   ```
   Find hotels in Tokyo for August 13-15, 2025
   ```
   Then respond with: `3` (to test hotel booking)

3. **Weather Information:**
   ```
   What's the weather in Tokyo on August 10, 2025?
   ```

4. **Travel Recommendations - Major City:**
   ```
   Give me travel recommendations for Paris
   ```

5. **Travel Recommendations - Small City:**
   ```
   Give me travel recommendations for Springfield, Illinois
   ```

6. **Trip Summary:**
   ```
   Give me a summary of my trip
   ```

### Manual Testing Checklist
- [ ] Real flight searches with future dates
- [ ] Flight booking workflow with confirmation
- [ ] Hotel data from Amadeus API
- [ ] Hotel booking workflow with confirmation
- [ ] Weather forecasts for various cities
- [ ] Travel recommendations with proper formatting
- [ ] Trip summary generation
- [ ] Fallback systems with unsupported locations
- [ ] Error handling for API failures

### Example Test Queries
- "Find flights from DFW to DEL for August 10-20, 2025"
- "Show me hotels in Dallas for next month"
- "What's the weather in New York today?"
- "Give me recommendations for activities in London"
- "Book a flight from LAX to JFK for next week"

## 🎨 UI/UX Improvements

### Recent Enhancements
- **Beautiful Flight Display**: Separate outbound/return flights with clear formatting
- **Hotel Selection Interface**: Numbered options with booking prompts
- **Improved Travel Recommendations**: Proper line breaks and bullet points
- **Enhanced Trip Summaries**: Emoji-rich formatting with clear sections
- **Better Error Handling**: Graceful fallbacks and user-friendly messages
- **Responsive Design**: Works well on desktop and mobile devices

### Formatting Standards
- **Flight Options**: Always show airline names, flight numbers, routes, and prices
- **Hotel Options**: Display ratings, locations, prices, and amenities clearly
- **Travel Recommendations**: Use bullet points and proper spacing
- **Trip Summaries**: Include all costs, dates, and important reminders

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
The application can be deployed to:
- **Heroku**: Using the provided `runtime.txt` and `setup.py`
- **Streamlit Cloud**: Direct deployment from GitHub
- **AWS/GCP**: Using Docker containers
- **Vercel**: With Python runtime

### Environment Variables
Ensure all required environment variables are set:
- `OPENAI_API_KEY`
- `AMADEUS_CLIENT_ID`
- `AMADEUS_CLIENT_SECRET`
- `OPENWEATHER_API_KEY`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Amadeus API**: For real flight and hotel data
- **OpenWeatherMap**: For weather information
- **DuckDuckGo**: For free web search capabilities
- **OpenAI**: For the GPT language model
- **LangChain**: For the agent framework
- **Streamlit**: For the web interface

---

**Built with ❤️ using Agentic AI principles** 

*Last Updated: July 2025* 