import os
from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents.agent import BaseSingleActionAgent
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
            agent=self.agent,  # type: ignore
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

        # @tool
        # def search_hotels(city: str, check_in: str, check_out: str, guests: int = 1) -> str:
        #     """Search for available hotels in a specific city.
        #     
        #     Args:
        #         city: City name (e.g., 'Paris', 'Tokyo', 'New York')
        #         check_in: Check-in date in YYYY-MM-DD format
        #         check_out: Check-out date in YYYY-MM-DD format
        #         guests: Number of guests (default: 1)
        #     
        #     Returns:
        #         String with hotel options and prices
        #     """
        #     # Simulate hotel search - in a real app, this would call a hotel API
        #     hotels = [
        #         {"name": "Grand Hotel", "rating": 4.5, "location": "City Center", "price": 200, "amenities": ["WiFi", "Pool", "Spa", "Restaurant"]},
        #         {"name": "Comfort Inn", "rating": 3.8, "location": "Airport Area", "price": 120, "amenities": ["WiFi", "Breakfast", "Parking"]},
        #         {"name": "Luxury Resort", "rating": 4.9, "location": "Beachfront", "price": 350, "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Gym", "Beach Access"]},
        #         {"name": "City Suites", "rating": 4.2, "location": "Business District", "price": 180, "amenities": ["WiFi", "Gym", "Breakfast"]},
        #         {"name": "Budget Stay", "rating": 3.5, "location": "Suburbs", "price": 90, "amenities": ["WiFi", "Parking"]},
        #         {"name": "Boutique Escape", "rating": 4.7, "location": "Old Town", "price": 270, "amenities": ["WiFi", "Spa", "Restaurant", "Bar"]}
        #     ]
        #     
        #     # Calculate number of nights
        #     from datetime import datetime
        #     check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        #     check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        #     nights = (check_out_date - check_in_date).days
        #     
        #     result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights):\n"
        #     
        #     for i, hotel in enumerate(hotels, 1):
        #         total_price = hotel["price"] * nights
        #         result += f"{i}. {hotel['name']} ({hotel['rating']}★)\n"
        #         result += f"   Location: {hotel['location']}\n"
        #         result += f"   Price per night: ${hotel['price']}\n"
        #         result += f"   Total for {nights} nights: ${total_price}\n"
        #         result += f"   Amenities: {', '.join(hotel['amenities'])}\n\n"
        #     
        #     return result

        @tool
        def search_hotels_amadeus(city: str, check_in: str, check_out: str, guests: int = 1) -> str:
            """Search for available hotels in a specific city using Amadeus API.
            Args:
                city: City name (e.g., 'Paris', 'Tokyo', 'New York')
                check_in: Check-in date in YYYY-MM-DD format
                check_out: Check-out date in YYYY-MM-DD format
                guests: Number of guests (default: 1)
            Returns:
                String with hotel options and prices
            """
            import requests
            import os
            from datetime import datetime
            
            # Get Amadeus credentials
            client_id = os.getenv("AMADEUS_CLIENT_ID")
            client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
            
            if not client_id or not client_secret:
                return "Amadeus API credentials not found. Please check your .env file."
            
            try:
                # Get access token
                token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
                token_data = {
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret
                }
                
                token_response = requests.post(token_url, data=token_data)
                if token_response.status_code != 200:
                    return f"Failed to get access token: {token_response.status_code}"
                
                access_token = token_response.json()["access_token"]
                
                # Search for hotels
                headers = {"Authorization": f"Bearer {access_token}"}
                
                # First, get the city code using the city search API
                city_search_url = "https://test.api.amadeus.com/v1/reference-data/locations"
                
                # Try different city name variations
                city_variations = [city, f"{city} City", f"{city} Metropolitan Area"]
                city_code = None
                
                for city_variant in city_variations:
                    city_params = {
                        "subType": "CITY",
                        "keyword": city_variant,
                        "page[limit]": 5  # Get more results to find the right city
                    }
                    
                    city_response = requests.get(city_search_url, headers=headers, params=city_params)
                    if city_response.status_code == 200:
                        city_data = city_response.json()
                        if city_data.get("data"):
                            # Find the best match
                            for location in city_data["data"]:
                                if location.get("address", {}).get("cityName", "").lower() == city.lower():
                                    city_code = location["address"]["cityCode"]
                                    break
                            if city_code:
                                break
                
                if not city_code:
                    # Comprehensive fallback with city-specific hotels
                    from datetime import datetime
                    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
                    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
                    nights = (check_out_date - check_in_date).days
                    
                    city_lower = city.lower().strip()
                    
                    # Tokyo-specific hotels
                    if 'tokyo' in city_lower:
                        hotels = [
                            {"name": "Park Hyatt Tokyo", "rating": 4.8, "location": "Shinjuku", "price": 450, "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "City View"]},
                            {"name": "Aman Tokyo", "rating": 4.9, "location": "Otemachi", "price": 800, "amenities": ["WiFi", "Spa", "Restaurant", "Gym", "Concierge"]},
                            {"name": "Hotel Gracery Shinjuku", "rating": 4.2, "location": "Shinjuku", "price": 180, "amenities": ["WiFi", "Restaurant", "Bar", "Convenience Store"]},
                            {"name": "Shibuya Excel Hotel", "rating": 4.0, "location": "Shibuya", "price": 150, "amenities": ["WiFi", "Restaurant", "Business Center"]},
                            {"name": "Hotel Century Southern Tower", "rating": 4.3, "location": "Shinjuku", "price": 200, "amenities": ["WiFi", "Restaurant", "Bar", "City View"]},
                            {"name": "Shinjuku Prince Hotel", "rating": 3.8, "location": "Shinjuku", "price": 120, "amenities": ["WiFi", "Restaurant", "Bar", "Movie Theater"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # Paris-specific hotels
                    elif 'paris' in city_lower:
                        hotels = [
                            {"name": "The Ritz Paris", "rating": 4.9, "location": "Place Vendôme", "price": 1200, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Concierge", "Historic"]},
                            {"name": "Hotel de Crillon", "rating": 4.8, "location": "Place de la Concorde", "price": 1000, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Pool", "Luxury"]},
                            {"name": "Le Bristol Paris", "rating": 4.7, "location": "Rue du Faubourg Saint-Honoré", "price": 800, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Pool", "Garden"]},
                            {"name": "Hotel Plaza Athénée", "rating": 4.6, "location": "Avenue Montaigne", "price": 900, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Eiffel View"]},
                            {"name": "Le Meurice", "rating": 4.5, "location": "Rue de Rivoli", "price": 750, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Tuileries View"]},
                            {"name": "Hotel Lutetia", "rating": 4.4, "location": "Left Bank", "price": 400, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Historic"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # London-specific hotels
                    elif 'london' in city_lower:
                        hotels = [
                            {"name": "The Savoy", "rating": 4.9, "location": "Strand", "price": 800, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "River View", "Historic"]},
                            {"name": "Claridge's", "rating": 4.8, "location": "Mayfair", "price": 900, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Afternoon Tea", "Luxury"]},
                            {"name": "The Connaught", "rating": 4.7, "location": "Mayfair", "price": 850, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Aman Spa"]},
                            {"name": "The Dorchester", "rating": 4.6, "location": "Park Lane", "price": 750, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Hyde Park View"]},
                            {"name": "Brown's Hotel", "rating": 4.5, "location": "Mayfair", "price": 600, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Historic"]},
                            {"name": "The Goring", "rating": 4.4, "location": "Belgravia", "price": 500, "amenities": ["WiFi", "Restaurant", "Bar", "Garden", "Royal Warrant"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # New York-specific hotels
                    elif 'new york' in city_lower or 'nyc' in city_lower:
                        hotels = [
                            {"name": "The Plaza", "rating": 4.8, "location": "Central Park South", "price": 600, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Central Park View", "Historic"]},
                            {"name": "Waldorf Astoria", "rating": 4.7, "location": "Park Avenue", "price": 550, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Art Deco", "Luxury"]},
                            {"name": "The St. Regis", "rating": 4.6, "location": "Fifth Avenue", "price": 700, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Butler Service"]},
                            {"name": "The Peninsula", "rating": 4.5, "location": "Fifth Avenue", "price": 650, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Rooftop Pool"]},
                            {"name": "The Carlyle", "rating": 4.4, "location": "Upper East Side", "price": 500, "amenities": ["WiFi", "Restaurant", "Bar", "Bemelmans Bar", "Historic"]},
                            {"name": "The Mark", "rating": 4.3, "location": "Upper East Side", "price": 450, "amenities": ["WiFi", "Restaurant", "Bar", "Jean-Georges", "Modern"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # Rome-specific hotels
                    elif 'rome' in city_lower:
                        hotels = [
                            {"name": "Hotel de Russie", "rating": 4.8, "location": "Piazza del Popolo", "price": 600, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Garden", "Historic"]},
                            {"name": "Hassler Roma", "rating": 4.7, "location": "Piazza Trinità dei Monti", "price": 700, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Spanish Steps View"]},
                            {"name": "Hotel Eden", "rating": 4.6, "location": "Via Ludovisi", "price": 550, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "City View", "Dorchester Collection"]},
                            {"name": "Palazzo Manfredi", "rating": 4.5, "location": "Via Labicana", "price": 400, "amenities": ["WiFi", "Restaurant", "Bar", "Colosseum View"]},
                            {"name": "Hotel Raphael", "rating": 4.4, "location": "Piazza Navona", "price": 350, "amenities": ["WiFi", "Restaurant", "Bar", "Rooftop Terrace", "Historic"]},
                            {"name": "Hotel Locarno", "rating": 4.3, "location": "Via della Penna", "price": 300, "amenities": ["WiFi", "Restaurant", "Bar", "Art Nouveau", "Charming"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # Barcelona-specific hotels
                    elif 'barcelona' in city_lower:
                        hotels = [
                            {"name": "Hotel Arts Barcelona", "rating": 4.8, "location": "Port Olímpic", "price": 400, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Beach Access", "Ritz-Carlton"]},
                            {"name": "W Barcelona", "rating": 4.7, "location": "Barceloneta", "price": 350, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Beachfront", "Modern"]},
                            {"name": "Hotel Majestic", "rating": 4.6, "location": "Passeig de Gràcia", "price": 300, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Gaudí Architecture"]},
                            {"name": "Casa Fuster", "rating": 4.5, "location": "Passeig de Gràcia", "price": 280, "amenities": ["WiFi", "Restaurant", "Bar", "Modernist Building", "Historic"]},
                            {"name": "Hotel 1898", "rating": 4.4, "location": "La Rambla", "price": 250, "amenities": ["WiFi", "Restaurant", "Bar", "Rooftop Pool", "Colonial"]},
                            {"name": "Hotel Neri", "rating": 4.3, "location": "Gothic Quarter", "price": 200, "amenities": ["WiFi", "Restaurant", "Bar", "Historic Building", "Boutique"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # Generic fallback for other cities
                    else:
                        hotels = [
                            {"name": "Grand Hotel", "rating": 4.5, "location": "City Center", "price": 200, "amenities": ["WiFi", "Pool", "Spa", "Restaurant"]},
                            {"name": "Comfort Inn", "rating": 3.8, "location": "Airport Area", "price": 120, "amenities": ["WiFi", "Breakfast", "Parking"]},
                            {"name": "Luxury Resort", "rating": 4.9, "location": "Beachfront", "price": 350, "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Gym", "Beach Access"]},
                            {"name": "City Suites", "rating": 4.2, "location": "Business District", "price": 180, "amenities": ["WiFi", "Gym", "Breakfast"]},
                            {"name": "Budget Stay", "rating": 3.5, "location": "Suburbs", "price": 90, "amenities": ["WiFi", "Parking"]},
                            {"name": "Boutique Escape", "rating": 4.7, "location": "Old Town", "price": 270, "amenities": ["WiFi", "Spa", "Restaurant", "Bar"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Simulated Data]:\n"
                    
                    # Display hotel information
                    for i, hotel in enumerate(hotels, 1):
                        total_price = hotel["price"] * nights
                        result += f"{i}. {hotel['name']} ({hotel['rating']}★)\n"
                        result += f"   Location: {hotel['location']}\n"
                        result += f"   Price per night: ${hotel['price']}\n"
                        result += f"   Total for {nights} nights: ${total_price}\n"
                        result += f"   Amenities: {', '.join(hotel['amenities'])}\n\n"
                    
                    return result
                
                # Now search for hotels using Amadeus API - Hotel Reference Data
                hotel_search_url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
                hotel_params = {
                    "cityCode": city_code,
                    "radius": 5,
                    "radiusUnit": "KM"
                }
                
                hotel_response = requests.get(hotel_search_url, headers=headers, params=hotel_params)
                if hotel_response.status_code != 200:
                    # Enhanced fallback with city-specific hotels when Amadeus hotel search fails
                    from datetime import datetime
                    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
                    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
                    nights = (check_out_date - check_in_date).days
                    
                    city_lower = city.lower().strip()
                    
                    # Tokyo-specific hotels
                    if 'tokyo' in city_lower:
                        hotels = [
                            {"name": "Park Hyatt Tokyo", "rating": 4.8, "location": "Shinjuku", "price": 450, "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "City View"]},
                            {"name": "Aman Tokyo", "rating": 4.9, "location": "Otemachi", "price": 800, "amenities": ["WiFi", "Spa", "Restaurant", "Gym", "Concierge"]},
                            {"name": "Hotel Gracery Shinjuku", "rating": 4.2, "location": "Shinjuku", "price": 180, "amenities": ["WiFi", "Restaurant", "Bar", "Convenience Store"]},
                            {"name": "Shibuya Excel Hotel", "rating": 4.0, "location": "Shibuya", "price": 150, "amenities": ["WiFi", "Restaurant", "Business Center"]},
                            {"name": "Hotel Century Southern Tower", "rating": 4.3, "location": "Shinjuku", "price": 200, "amenities": ["WiFi", "Restaurant", "Bar", "City View"]},
                            {"name": "Shinjuku Prince Hotel", "rating": 3.8, "location": "Shinjuku", "price": 120, "amenities": ["WiFi", "Restaurant", "Bar", "Movie Theater"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # Paris-specific hotels
                    elif 'paris' in city_lower:
                        hotels = [
                            {"name": "The Ritz Paris", "rating": 4.9, "location": "Place Vendôme", "price": 1200, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Concierge", "Historic"]},
                            {"name": "Hotel de Crillon", "rating": 4.8, "location": "Place de la Concorde", "price": 1000, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Pool", "Luxury"]},
                            {"name": "Le Bristol Paris", "rating": 4.7, "location": "Rue du Faubourg Saint-Honoré", "price": 800, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Pool", "Garden"]},
                            {"name": "Hotel Plaza Athénée", "rating": 4.6, "location": "Avenue Montaigne", "price": 900, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Eiffel View"]},
                            {"name": "Le Meurice", "rating": 4.5, "location": "Rue de Rivoli", "price": 750, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Tuileries View"]},
                            {"name": "Hotel Lutetia", "rating": 4.4, "location": "Left Bank", "price": 400, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Historic"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # London-specific hotels
                    elif 'london' in city_lower:
                        hotels = [
                            {"name": "The Savoy", "rating": 4.9, "location": "Strand", "price": 800, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "River View", "Historic"]},
                            {"name": "Claridge's", "rating": 4.8, "location": "Mayfair", "price": 900, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Afternoon Tea", "Luxury"]},
                            {"name": "The Connaught", "rating": 4.7, "location": "Mayfair", "price": 850, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Aman Spa"]},
                            {"name": "The Dorchester", "rating": 4.6, "location": "Park Lane", "price": 750, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Hyde Park View"]},
                            {"name": "Brown's Hotel", "rating": 4.5, "location": "Mayfair", "price": 600, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Historic"]},
                            {"name": "The Goring", "rating": 4.4, "location": "Belgravia", "price": 500, "amenities": ["WiFi", "Restaurant", "Bar", "Garden", "Royal Warrant"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # New York-specific hotels
                    elif 'new york' in city_lower or 'nyc' in city_lower:
                        hotels = [
                            {"name": "The Plaza", "rating": 4.8, "location": "Central Park South", "price": 600, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Central Park View", "Historic"]},
                            {"name": "Waldorf Astoria", "rating": 4.7, "location": "Park Avenue", "price": 550, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Art Deco", "Luxury"]},
                            {"name": "The St. Regis", "rating": 4.6, "location": "Fifth Avenue", "price": 700, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Butler Service"]},
                            {"name": "The Peninsula", "rating": 4.5, "location": "Fifth Avenue", "price": 650, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Rooftop Pool"]},
                            {"name": "The Carlyle", "rating": 4.4, "location": "Upper East Side", "price": 500, "amenities": ["WiFi", "Restaurant", "Bar", "Bemelmans Bar", "Historic"]},
                            {"name": "The Mark", "rating": 4.3, "location": "Upper East Side", "price": 450, "amenities": ["WiFi", "Restaurant", "Bar", "Jean-Georges", "Modern"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # Rome-specific hotels
                    elif 'rome' in city_lower:
                        hotels = [
                            {"name": "Hotel de Russie", "rating": 4.8, "location": "Piazza del Popolo", "price": 600, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Garden", "Historic"]},
                            {"name": "Hassler Roma", "rating": 4.7, "location": "Piazza Trinità dei Monti", "price": 700, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Spanish Steps View"]},
                            {"name": "Hotel Eden", "rating": 4.6, "location": "Via Ludovisi", "price": 550, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "City View", "Dorchester Collection"]},
                            {"name": "Palazzo Manfredi", "rating": 4.5, "location": "Via Labicana", "price": 400, "amenities": ["WiFi", "Restaurant", "Bar", "Colosseum View"]},
                            {"name": "Hotel Raphael", "rating": 4.4, "location": "Piazza Navona", "price": 350, "amenities": ["WiFi", "Restaurant", "Bar", "Rooftop Terrace", "Historic"]},
                            {"name": "Hotel Locarno", "rating": 4.3, "location": "Via della Penna", "price": 300, "amenities": ["WiFi", "Restaurant", "Bar", "Art Nouveau", "Charming"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # Barcelona-specific hotels
                    elif 'barcelona' in city_lower:
                        hotels = [
                            {"name": "Hotel Arts Barcelona", "rating": 4.8, "location": "Port Olímpic", "price": 400, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Beach Access", "Ritz-Carlton"]},
                            {"name": "W Barcelona", "rating": 4.7, "location": "Barceloneta", "price": 350, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Beachfront", "Modern"]},
                            {"name": "Hotel Majestic", "rating": 4.6, "location": "Passeig de Gràcia", "price": 300, "amenities": ["WiFi", "Spa", "Restaurant", "Bar", "Gaudí Architecture"]},
                            {"name": "Casa Fuster", "rating": 4.5, "location": "Passeig de Gràcia", "price": 280, "amenities": ["WiFi", "Restaurant", "Bar", "Modernist Building", "Historic"]},
                            {"name": "Hotel 1898", "rating": 4.4, "location": "La Rambla", "price": 250, "amenities": ["WiFi", "Restaurant", "Bar", "Rooftop Pool", "Colonial"]},
                            {"name": "Hotel Neri", "rating": 4.3, "location": "Gothic Quarter", "price": 200, "amenities": ["WiFi", "Restaurant", "Bar", "Historic Building", "Boutique"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Local Recommendations]:\n"
                    
                    # Generic fallback for other cities
                    else:
                        hotels = [
                            {"name": "Grand Hotel", "rating": 4.5, "location": "City Center", "price": 200, "amenities": ["WiFi", "Pool", "Spa", "Restaurant"]},
                            {"name": "Comfort Inn", "rating": 3.8, "location": "Airport Area", "price": 120, "amenities": ["WiFi", "Breakfast", "Parking"]},
                            {"name": "Luxury Resort", "rating": 4.9, "location": "Beachfront", "price": 350, "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Gym", "Beach Access"]},
                            {"name": "City Suites", "rating": 4.2, "location": "Business District", "price": 180, "amenities": ["WiFi", "Gym", "Breakfast"]},
                            {"name": "Budget Stay", "rating": 3.5, "location": "Suburbs", "price": 90, "amenities": ["WiFi", "Parking"]},
                            {"name": "Boutique Escape", "rating": 4.7, "location": "Old Town", "price": 270, "amenities": ["WiFi", "Spa", "Restaurant", "Bar"]}
                        ]
                        result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Simulated Data]:\n"
                    
                    # Display hotel information
                    for i, hotel in enumerate(hotels, 1):
                        total_price = hotel["price"] * nights
                        result += f"{i}. {hotel['name']} ({hotel['rating']}★)\n"
                        result += f"   Location: {hotel['location']}\n"
                        result += f"   Price per night: ${hotel['price']}\n"
                        result += f"   Total for {nights} nights: ${total_price}\n"
                        result += f"   Amenities: {', '.join(hotel['amenities'])}\n\n"
                    
                    return result
                
                hotel_data = hotel_response.json()
                hotels = hotel_data.get("data", [])
                
                if not hotels:
                    return f"No hotels found in {city} for the specified dates."
                
                # Calculate number of nights
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
                nights = (check_out_date - check_in_date).days
                
                result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Amadeus API]:\n"
                
                for i, hotel in enumerate(hotels[:6], 1):  # Limit to 6 hotels
                    # Get hotel details from reference data
                    name = hotel.get("name", "Unknown Hotel")
                    chain_code = hotel.get("chainCode", "")
                    iata_code = hotel.get("iataCode", "")
                    hotel_id = hotel.get("hotelId", "")
                    
                    # Get location info
                    geo_code = hotel.get("geoCode", {})
                    latitude = geo_code.get("latitude", "")
                    longitude = geo_code.get("longitude", "")
                    
                    # Get distance info
                    distance = hotel.get("distance", {})
                    distance_value = distance.get("value", "")
                    distance_unit = distance.get("unit", "KM")
                    
                    # Get address info
                    address = hotel.get("address", {})
                    country_code = address.get("countryCode", "")
                    
                    # Since this is reference data, we don't have pricing or amenities
                    # We'll use estimated pricing based on hotel type
                    estimated_price = 200  # Default estimated price
                    if chain_code in ["HI", "AC", "CP"]:  # Holiday Inn, Accor, Choice
                        estimated_price = 150
                    elif chain_code in ["MA", "RI", "SH"]:  # Marriott, Ritz, Sheraton
                        estimated_price = 300
                    elif chain_code in ["ZZ", "NN"]:  # Independent hotels
                        estimated_price = 180
                    
                    total_price = estimated_price * nights
                    
                    result += f"{i}. {name}\n"
                    result += f"   Chain: {chain_code} | IATA: {iata_code}\n"
                    result += f"   Location: {city}, {country_code}\n"
                    result += f"   Distance: {distance_value} {distance_unit} from city center\n"
                    result += f"   Estimated Price: ${estimated_price} per night\n"
                    result += f"   Total for {nights} nights: ${total_price}\n"
                    result += f"   Coordinates: {latitude}, {longitude}\n\n"
                
                return result

            except Exception as e:
                # Fallback to simulated hotel data if Amadeus API fails
                try:
                    from datetime import datetime
                    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
                    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
                    nights = (check_out_date - check_in_date).days
                    
                    # Simulated hotel data as fallback
                    hotels = [
                        {"name": "Grand Hotel", "rating": 4.5, "location": "City Center", "price": 200, "amenities": ["WiFi", "Pool", "Spa", "Restaurant"]},
                        {"name": "Comfort Inn", "rating": 3.8, "location": "Airport Area", "price": 120, "amenities": ["WiFi", "Breakfast", "Parking"]},
                        {"name": "Luxury Resort", "rating": 4.9, "location": "Beachfront", "price": 350, "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Gym", "Beach Access"]},
                        {"name": "City Suites", "rating": 4.2, "location": "Business District", "price": 180, "amenities": ["WiFi", "Gym", "Breakfast"]},
                        {"name": "Budget Stay", "rating": 3.5, "location": "Suburbs", "price": 90, "amenities": ["WiFi", "Parking"]},
                        {"name": "Boutique Escape", "rating": 4.7, "location": "Old Town", "price": 270, "amenities": ["WiFi", "Spa", "Restaurant", "Bar"]}
                    ]
                    
                    result = f"Found {len(hotels)} hotels in {city} from {check_in} to {check_out} ({nights} nights) [Simulated Data]:\n"
                    
                    for i, hotel in enumerate(hotels, 1):
                        total_price = hotel["price"] * nights
                        result += f"{i}. {hotel['name']} ({hotel['rating']}★)\n"
                        result += f"   Location: {hotel['location']}\n"
                        result += f"   Price per night: ${hotel['price']}\n"
                        result += f"   Total for {nights} nights: ${total_price}\n"
                        result += f"   Amenities: {', '.join(hotel['amenities'])}\n\n"
                    
                    return result
                except:
                    return f"Error searching hotels: {str(e)}"

        @tool
        def get_weather_forecast(city: str, date: Optional[str] = None) -> str:
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
                city: City name (e.g., 'Paris', 'Tokyo', 'New York', 'Aspen', 'Colorado')
                interests: Type of interests (e.g., 'culture', 'food', 'adventure', 'shopping', 'outdoors')
            
            Returns:
                String with travel recommendations
            """
            import requests
            import re
            
            # First, try to get web search results for travel recommendations
            try:
                # Use DuckDuckGo Instant Answer API (free, no API key needed)
                search_query = f"{city} travel guide attractions restaurants activities"
                search_url = "https://api.duckduckgo.com/"
                params = {
                    "q": search_query,
                    "format": "json",
                    "no_html": "1",
                    "skip_disambig": "1"
                }
                
                response = requests.get(search_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract information from the response
                    abstract = data.get("Abstract", "")
                    related_topics = data.get("RelatedTopics", [])
                    
                    # Build recommendations from web data
                    result = f"Travel recommendations for {city}:\n\n"
                    
                    # Add abstract if available
                    if abstract:
                        result += f"Overview: {abstract}\n\n"
                    
                    # Extract attractions and activities from related topics
                    attractions = []
                    activities = []
                    restaurants = []
                    tips = []
                    
                    for topic in related_topics[:10]:  # Limit to first 10 topics
                        if isinstance(topic, dict) and "Text" in topic:
                            text = topic["Text"]
                            # Categorize based on keywords
                            if any(keyword in text.lower() for keyword in ["museum", "park", "tower", "palace", "temple", "monument", "landmark"]):
                                attractions.append(text)
                            elif any(keyword in text.lower() for keyword in ["restaurant", "cafe", "dining", "food", "cuisine"]):
                                restaurants.append(text)
                            elif any(keyword in text.lower() for keyword in ["hiking", "skiing", "swimming", "tour", "walking", "adventure"]):
                                activities.append(text)
                            else:
                                tips.append(text)
                    
                    # Add categorized recommendations
                    if attractions:
                        result += "Top Attractions:\n"
                        for i, attraction in enumerate(attractions[:5], 1):
                            result += f"{i}. {attraction}\n"
                        result += "\n"
                    
                    if restaurants:
                        result += "Recommended Restaurants:\n"
                        for i, restaurant in enumerate(restaurants[:3], 1):
                            result += f"{i}. {restaurant}\n"
                        result += "\n"
                    
                    if activities:
                        result += "Popular Activities:\n"
                        for i, activity in enumerate(activities[:3], 1):
                            result += f"{i}. {activity}\n"
                        result += "\n"
                    
                    if tips:
                        result += "Travel Tips:\n"
                        for i, tip in enumerate(tips[:3], 1):
                            result += f"{i}. {tip}\n"
                    
                    # If we got some data, return it
                    if abstract or attractions or activities or restaurants:
                        return result
                
            except Exception as e:
                # If web search fails, continue to fallback
                pass
            
            # Fallback to curated recommendations for major cities
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
                },
                "London": {
                    "attractions": ["Big Ben", "Tower of London", "Buckingham Palace", "British Museum"],
                    "restaurants": ["The Fat Duck", "Gordon Ramsay", "Sketch"],
                    "activities": ["Thames River Cruise", "West End Show", "Changing of the Guard"],
                    "tips": ["Get an Oyster card for public transport", "Book attractions in advance"]
                },
                "Rome": {
                    "attractions": ["Colosseum", "Vatican Museums", "Trevi Fountain", "Pantheon"],
                    "restaurants": ["La Pergola", "Il Pagliaccio", "Aroma"],
                    "activities": ["Vatican Tour", "Roman Forum Walk", "Gelato Tasting"],
                    "tips": ["Book Vatican tickets online to skip lines", "Visit early morning to avoid crowds"]
                },
                "Barcelona": {
                    "attractions": ["Sagrada Familia", "Park Güell", "Casa Batlló", "La Rambla"],
                    "restaurants": ["El Celler de Can Roca", "Tickets", "Disfrutar"],
                    "activities": ["Gaudi Architecture Tour", "Tapas Crawl", "Beach Day"],
                    "tips": ["Book Sagrada Familia tickets in advance", "Learn basic Catalan phrases"]
                },
                "Aspen": {
                    "attractions": ["Aspen Mountain", "Maroon Bells", "Aspen Art Museum", "Wheeler Opera House"],
                    "restaurants": ["Element 47", "Cache Cache", "Matsuhisa"],
                    "activities": ["Skiing/Snowboarding", "Hiking Maroon Bells", "Hot Springs"],
                    "tips": ["Visit during shoulder seasons for better deals", "Book ski passes in advance"]
                },
                "Colorado": {
                    "attractions": ["Rocky Mountain National Park", "Garden of the Gods", "Mesa Verde", "Pikes Peak"],
                    "restaurants": ["Fruition", "Acorn", "Mercantile"],
                    "activities": ["Hiking", "Rock Climbing", "White Water Rafting", "Skiing"],
                    "tips": ["Check weather conditions before outdoor activities", "Get altitude acclimation"]
                }
            }
            
            # Check if we have curated data for this city
            if city in recommendations:
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
            
            # If no curated data and web search failed, provide a generic response
            return f"I found some general information about {city}, but for the most comprehensive and up-to-date travel recommendations, I recommend checking travel websites like TripAdvisor, Lonely Planet, or the official tourism website for {city}. You can also ask me about specific aspects like weather, flights, or hotels for {city}."
        
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
        
        return [search_hotels_amadeus, get_weather_forecast, get_travel_recommendations, search_flights_amadeus]
    
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