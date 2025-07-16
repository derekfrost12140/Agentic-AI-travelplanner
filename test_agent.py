#!/usr/bin/env python3
"""
Simple test script for the AI Travel Agent
Run this to verify the core functionality works before using the Streamlit app
"""

import os
from travel_agent import TravelAgent

def test_travel_agent():
    """Test the travel agent with sample queries"""
    
    print("🧪 Testing AI Travel Agent...")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize the agent
        print("🔧 Initializing Travel Agent...")
        agent = TravelAgent()
        print("✅ Travel Agent initialized successfully!")
        
        # Test queries
        test_queries = [
            "What's the weather like in Paris tomorrow?",
            "Find flights from New York to Tokyo for next week",
            "Search for hotels in London for March 15-20",
            "Give me travel recommendations for Tokyo"
        ]
        
        print("\n📝 Running test queries...")
        print("-" * 50)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            print("-" * 30)
            
            try:
                response = agent.chat(query)
                print(f"✅ Response received ({len(response)} characters)")
                print(f"📄 Response preview: {response[:200]}...")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed!")
        print("✅ The AI Travel Agent is working correctly")
        print("🚀 You can now run 'streamlit run app.py' to start the web interface")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize Travel Agent: {str(e)}")
        return False

if __name__ == "__main__":
    test_travel_agent() 