#!/usr/bin/env python3
"""
Demo script for AI Travel Agent
This script demonstrates the agent's capabilities with predefined examples
"""

import os
from travel_agent import TravelAgent
import time

def run_demo():
    """Run a demonstration of the AI Travel Agent"""
    
    print("🎬 AI Travel Agent Demo")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ Please set your OpenAI API key first")
        print("📝 Edit the .env file and add your API key")
        return
    
    try:
        # Initialize agent
        print("🔧 Initializing AI Travel Agent...")
        agent = TravelAgent()
        print("✅ Agent ready!")
        
        # Demo scenarios
        scenarios = [
            {
                "title": "🌍 Complete Trip Planning",
                "query": "I want to plan a 7-day romantic getaway to Paris for next month. I'm traveling with my partner and we love culture, food, and art. Our budget is around $3000. Can you help me plan everything?",
                "description": "This demonstrates the agent's ability to understand complex requirements and coordinate multiple tools."
            },
            {
                "title": "✈️ Flight Search",
                "query": "I need to find flights from San Francisco to Tokyo for business travel next week. I prefer morning departures and need to be there by Tuesday.",
                "description": "Shows the agent's flight search capabilities with specific preferences."
            },
            {
                "title": "🏨 Hotel Recommendations",
                "query": "Find me luxury hotels in New York City for a 4-night stay from March 20-24. I want something in Manhattan with a spa and good restaurants nearby.",
                "description": "Demonstrates hotel search with specific requirements and preferences."
            },
            {
                "title": "🌤️ Weather Information",
                "query": "What's the weather forecast for London this weekend? I'm planning outdoor activities.",
                "description": "Shows weather information retrieval capabilities."
            },
            {
                "title": "🎯 Travel Recommendations",
                "query": "I'm visiting Tokyo for the first time. What are the must-see attractions, best restaurants, and unique experiences I shouldn't miss?",
                "description": "Demonstrates the agent's knowledge base and recommendation system."
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{'='*60}")
            print(f"🎭 Demo {i}: {scenario['title']}")
            print(f"📝 {scenario['description']}")
            print(f"{'='*60}")
            
            print(f"\n👤 User: {scenario['query']}")
            print("\n🤖 AI Travel Agent is thinking...")
            
            # Get response
            start_time = time.time()
            response = agent.chat(scenario['query'])
            end_time = time.time()
            
            print(f"\n🤖 AI Travel Agent (response time: {end_time - start_time:.2f}s):")
            print("-" * 40)
            print(response)
            print("-" * 40)
            
            # Pause between demos
            if i < len(scenarios):
                input("\n⏸️  Press Enter to continue to the next demo...")
        
        print(f"\n{'='*60}")
        print("🎉 Demo completed!")
        print("=" * 60)
        print("\n💡 Key Features Demonstrated:")
        print("✅ Multi-tool coordination")
        print("✅ Natural language understanding")
        print("✅ Contextual responses")
        print("✅ Travel-specific knowledge")
        print("✅ Real-time information retrieval")
        
        print("\n🚀 To try it yourself:")
        print("1. Run 'streamlit run app.py' for the web interface")
        print("2. Or use the agent programmatically in your own code")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Please check your API key and internet connection")

if __name__ == "__main__":
    run_demo() 