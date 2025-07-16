import os
from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta
from dateutil import parser as date_parser

# Load environment variables
load_dotenv()

class TravelAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _create_tools(self) -> List:
        """Create tools for the travel agent"""
        
        # @tool
        # def search_flights(origin: str, destination: str, date: str, passengers: int = 1) -> str:
        #     """Search for available flights between two cities on a specific date.
        #     
        #     Args:
        #         origin: Departure city (e.g., 'New York', 'London')
        #         destination: Arrival city (e.g., 'Paris', 'Tokyo')
        #         date: Travel date in YYYY-MM-DD format
        #         passengers: Number of passengers (default: 1)
        #     
        #     Returns:
        #         String with flight options and prices
        #     """
        #     # Simulate flight search - in a real app, this would call a flight API
        #     flights = [
        #         {"airline": "Delta Airlines", "flight_number": "DL123", "departure": "08:00", "arrival": "11:30", "price": 450, "duration": "3h 30m"},
        #         {"airline": "American Airlines", "flight_number": "AA456", "departure": "14:15", "arrival": "17:45", "price": 380, "duration": "3h 30m"},
        #         {"airline": "United Airlines", "flight_number": "UA789", "departure": "20:30", "arrival": "23:45", "price": 520, "duration": "3h 15m"},
        #         {"airline": "British Airways", "flight_number": "BA321", "departure": "10:00", "arrival": "13:20", "price": 410, "duration": "3h 20m"},
        #         {"airline": "Air France", "flight_number": "AF654", "departure": "16:45", "arrival": "20:05", "price": 470, "duration": "3h 20m"},
        #         {"airline": "Lufthansa", "flight_number": "LH987", "departure": "06:30", "arrival": "09:50", "price": 395, "duration": "3h 20m"}
        #     ]
        #     result = f"Found {len(flights)} flights from {origin} to {destination} on {date}:\n\n"
        #     for i, flight in enumerate(flights, 1):
        #         result += f"{i}. {flight['airline']} {flight['flight_number']}\n"
        #         result += f"   Departure: {flight['departure']} | Arrival: {flight['arrival']}\n"
        #         result += f"   Duration: {flight['duration']} | Price: ${flight['price']}\n\n"
        #     return result

        @tool
        def search_hotels(city: str, check_in: str, check_out: str, guests: int = 2) -> str:
            """Search for available hotels in a specific city.
            
            Args:
                city: City name (e.g., 'Paris', 'Tokyo', 'New York')
                check_in: Check-in date in YYYY-MM-DD format
                check_out: Check-out date in YYYY-MM-DD format
                guests: Number of guests (default: 2)
            
            Returns:
                String with hotel options and prices
            """
            # Simulate hotel search - in a real app, this would call a hotel API
            hotels = [
                {"name": "Grand Hotel", "rating": 4.5, "price_per_night": 200, "amenities": ["WiFi", "Pool", "Spa", "Restaurant"], "location": "City Center"},
                {"name": "Comfort Inn", "rating": 3.8, "price_per_night": 120, "amenities": ["WiFi", "Breakfast", "Parking"], "location": "Airport Area"},
                {"name": "Luxury Resort", "rating": 4.9, "price_per_night": 350, "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Gym", "Beach Access"], "location": "Beachfront"},
                {"name": "City Suites", "rating": 4.2, "price_per_night": 180, "amenities": ["WiFi", "Gym", "Breakfast"], "location": "Business District"},
                {"name": "Budget Stay", "rating": 3.5, "price_per_night": 90, "amenities": ["WiFi", "Parking"], "location": "Suburbs"},
                {"name": "Boutique Escape", "rating": 4.7, "price_per_night": 270, "amenities": ["WiFi", "Spa", "Restaurant", "Bar"], "location": "Old Town"}
            ]
            nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights):\n\n"
            for i, hotel in enumerate(hotels, 1):
                total_price = hotel['price_per_night'] * nights
                result += f"{i}. {hotel['name']} ({hotel['rating']}★)\n"
                result += f"   Location: {hotel['location']}\n"
                result += f"   Price per night: ${hotel['price_per_night']}\n"
                result += f"   Total for {nights} nights: ${total_price}\n"
                result += f"   Amenities: {', '.join(hotel['amenities'])}\n\n"
            return result

        @tool
        def get_weather_forecast(city: str, date: str = None) -> str:
            """Get real-time weather forecast for a specific city using OpenWeatherMap API.
            Args:
                city: City name (e.g., 'Paris', 'Tokyo', 'New York')
                date: Date in YYYY-MM-DD format (optional, only current and forecast weather is supported)
            Returns:
                String with weather information
            """
            if not city or not isinstance(city, str):
                return "Please provide a valid city name as a string."
            import requests
            import os
            from datetime import datetime
            api_key = os.getenv("OPENWEATHER_API_KEY")
            if not api_key:
                return "OpenWeatherMap API key is missing. Please set OPENWEATHER_API_KEY in your .env file."
            # Step 1: Get latitude and longitude for the city
            geo_url = "http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {"q": city, "limit": 1, "appid": api_key}
            geo_resp = requests.get(geo_url, params=geo_params)
            geo_data = geo_resp.json()
            if not geo_data or geo_data[0].get("lat") is None or geo_data[0].get("lon") is None:
                return f"Could not find coordinates for {city}."
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]
            # Step 2: Get weather forecast
            forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
            forecast_params = {"lat": lat, "lon": lon, "appid": api_key, "units": "imperial"}
            forecast_resp = requests.get(forecast_url, params=forecast_params)
            if forecast_resp.status_code != 200:
                return f"API error: {forecast_resp.status_code} - {forecast_resp.text}"
            forecast_data = forecast_resp.json()
            forecasts = forecast_data.get("list", [])
            if not forecasts:
                return f"No forecast data available for {city}."
            # Date validation and selection
            now = datetime.now()
            if date:
                try:
                    target_date = datetime.strptime(date, "%Y-%m-%d")
                except Exception:
                    return "Invalid date format. Please use YYYY-MM-DD."
                if target_date.date() < now.date():
                    today_str = now.strftime('%Y-%m-%d')
                    return (f"Sorry, I can only provide weather forecasts for today or future dates. "
                            f"Please enter a valid date (today or later). For example, try: {today_str}.")
                # Find the forecast closest to the target date
                closest = min(forecasts, key=lambda f: abs(datetime.strptime(f["dt_txt"], "%Y-%m-%d %H:%M:%S") - target_date))
            else:
                closest = forecasts[0]
            dt_txt = closest["dt_txt"]
            temp = closest["main"]["temp"]
            weather = closest["weather"][0]["description"]
            return f"Weather forecast for {city} on {dt_txt}: {temp}°F, {weather}."
        
        @tool
        def get_travel_recommendations(city: str, interests: str = "general") -> str:
            """Get travel recommendations for a specific city based on interests.
            
            Args:
                city: City name (e.g., 'Paris', 'Tokyo', 'New York')
                interests: Type of interests (e.g., 'culture', 'food', 'adventure', 'shopping')
            
            Returns:
                String with travel recommendations
            """
            # Simulate recommendations - in a real app, this would use a knowledge base
            recommendations = {
                "Paris": {
                    "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Arc de Triomphe"],
                    "restaurants": ["Le Jules Verne", "L'Astrance", "Pierre Gagnaire"],
                    "activities": ["Seine River Cruise", "Montmartre Walking Tour", "Wine Tasting"],
                    "tips": ["Visit museums on first Sunday of month for free entry", "Book Eiffel Tower tickets in advance"]
                },
                "Tokyo": {
                    "attractions": ["Senso-ji Temple", "Tokyo Skytree", "Shibuya Crossing", "Tsukiji Fish Market"],
                    "restaurants": ["Sukiyabashi Jiro", "Narisawa", "Den"],
                    "activities": ["Cherry Blossom Viewing", "Robot Restaurant Show", "Traditional Tea Ceremony"],
                    "tips": ["Get a Japan Rail Pass for train travel", "Learn basic Japanese phrases"]
                },
                "New York": {
                    "attractions": ["Statue of Liberty", "Central Park", "Times Square", "Empire State Building"],
                    "restaurants": ["Le Bernardin", "Eleven Madison Park", "Per Se"],
                    "activities": ["Broadway Show", "Brooklyn Bridge Walk", "Museum of Modern Art"],
                    "tips": ["Get a MetroCard for subway access", "Book Broadway tickets in advance"]
                }
            }
            
            if city not in recommendations:
                return f"Sorry, I don't have specific recommendations for {city} yet."
            
            city_data = recommendations[city]
            result = f"Travel recommendations for {city}:\n\n"
            result += f"Top Attractions:\n"
            for i, attraction in enumerate(city_data["attractions"], 1):
                result += f"{i}. {attraction}\n"
            
            result += f"\nRecommended Restaurants:\n"
            for i, restaurant in enumerate(city_data["restaurants"], 1):
                result += f"{i}. {restaurant}\n"
            
            result += f"\nPopular Activities:\n"
            for i, activity in enumerate(city_data["activities"], 1):
                result += f"{i}. {activity}\n"
            
            result += f"\nTravel Tips:\n"
            for i, tip in enumerate(city_data["tips"], 1):
                result += f"{i}. {tip}\n"
            
            return result
        
        @tool
        def search_flights_amadeus(origin: str, destination: str, departure_date: str, return_date: str, adults: int = 1, currency: str = "USD") -> str:
            """Search for round-trip flights using Amadeus API.
            Args:
                origin: IATA code of departure airport (e.g., 'JFK')
                destination: IATA code of destination airport (e.g., 'LHR')
                departure_date: Outbound flight date (YYYY-MM-DD)
                return_date: Return flight date (YYYY-MM-DD)
                adults: Number of adult travelers
                currency: Preferred currency (default: USD)
            Returns:
                String summary of flight offers
            """
            import os
            import requests
            # Step 1: Get access token
            token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "grant_type": "client_credentials",
                "client_id": os.getenv("AMADEUS_CLIENT_ID"),
                "client_secret": os.getenv("AMADEUS_CLIENT_SECRET"),
            }
            token_resp = requests.post(token_url, headers=headers, data=data)
            if token_resp.status_code != 200:
                return f"Failed to get Amadeus access token: {token_resp.text}"
            access_token = token_resp.json().get("access_token")
            if not access_token:
                return "No access token received from Amadeus."
            # Step 2: Search for flight offers
            search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
            params = {
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": departure_date,
                "returnDate": return_date,
                "adults": adults,
                "currencyCode": currency,
                "max": 5
            }
            search_headers = {"Authorization": f"Bearer {access_token}"}
            search_resp = requests.get(search_url, headers=search_headers, params=params)
            if search_resp.status_code != 200:
                return f"Failed to get flight offers: {search_resp.text}"
            offers = search_resp.json().get("data", [])
            if not offers:
                return "No flight offers found. Try different dates or airports."
            # Summarize offers
            result = f"Found {len(offers)} round-trip flight offers from {origin} to {destination} (currency: {currency}):\n\n"
            for i, offer in enumerate(offers, 1):
                price = offer["price"]["total"]
                itineraries = offer["itineraries"]
                outbound_segments = itineraries[0]["segments"]
                inbound_segments = itineraries[1]["segments"] if len(itineraries) > 1 else []
                
                # Build outbound route (all segments)
                outbound_route = []
                for segment in outbound_segments:
                    departure = segment.get('departure', {})
                    arrival = segment.get('arrival', {})
                    airline = segment.get('carrierCode', 'N/A')
                    flight_number = segment.get('flightNumber') or segment.get('number', 'N/A')
                    # Format the departure date
                    departure_date = departure.get('at', 'N/A')
                    if departure_date != 'N/A':
                        try:
                            from datetime import datetime
                            date_obj = datetime.fromisoformat(departure_date.replace('Z', '+00:00'))
                            formatted_date = date_obj.strftime('%b %d')
                        except:
                            formatted_date = 'N/A'
                    else:
                        formatted_date = 'N/A'
                    outbound_route.append(f"{departure.get('iataCode', 'N/A')} → {arrival.get('iataCode', 'N/A')} ({airline} {flight_number}, {formatted_date})")
                
                # Build inbound route (all segments)
                inbound_route = []
                for segment in inbound_segments:
                    departure = segment.get('departure', {})
                    arrival = segment.get('arrival', {})
                    airline = segment.get('carrierCode', 'N/A')
                    flight_number = segment.get('flightNumber') or segment.get('number', 'N/A')
                    # Format the departure date
                    departure_date = departure.get('at', 'N/A')
                    if departure_date != 'N/A':
                        try:
                            from datetime import datetime
                            date_obj = datetime.fromisoformat(departure_date.replace('Z', '+00:00'))
                            formatted_date = date_obj.strftime('%b %d')
                        except:
                            formatted_date = 'N/A'
                    else:
                        formatted_date = 'N/A'
                    inbound_route.append(f"{departure.get('iataCode', 'N/A')} → {arrival.get('iataCode', 'N/A')} ({airline} {flight_number}, {formatted_date})")
                
                result += f"{i}. Outbound: {' → '.join(outbound_route)}\n"
                if inbound_route:
                    result += f"   Return: {' → '.join(inbound_route)}\n"
                result += f"   Total Price: {price} {currency}\n\n"
            return result
        
        return [search_hotels, get_weather_forecast, get_travel_recommendations, search_flights_amadeus]
    
    def _create_agent(self):
        """Create the agent with prompt template"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI Travel Agent assistant. Your job is to help users plan their trips by:

1. Understanding their travel requirements (destination, dates, budget, preferences)
2. Searching for flights, hotels, and activities
3. Providing weather information and travel recommendations
4. Creating comprehensive travel itineraries

Always be helpful, friendly, and provide detailed information. When users ask for travel planning, ask follow-up questions to understand their preferences better.

Use the available tools to search for flights, hotels, weather, and recommendations. Provide clear, organized responses with all relevant information."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        return create_openai_tools_agent(self.llm, self.tools, prompt)
    
    def chat(self, message: str, chat_history: Optional[List[BaseMessage]] = None) -> str:
        """Chat with the travel agent"""
        if chat_history is None:
            chat_history = []
        
        try:
            response = self.agent_executor.invoke({
                "input": message,
                "chat_history": chat_history
            })
            return response["output"]
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try rephrasing your request."

# Example usage
if __name__ == "__main__":
    agent = TravelAgent()
    response = agent.chat("I want to plan a trip to Paris for next month. Can you help me?")
    print(response) 