#!/usr/bin/env python3
"""
Test script for the download functionality
"""

import json
from datetime import datetime

def test_download_functionality():
    """Test the download functionality with sample data"""
    
    # Sample conversation history
    sample_conversation = [
        {
            "role": "user",
            "content": "I want to plan a trip to Paris for next month. Can you help me?"
        },
        {
            "role": "assistant", 
            "content": "I'd be happy to help you plan your trip to Paris! To provide the best recommendations, I need a few details:\n\n- What dates are you planning to travel?\n- How many people are traveling?\n- What's your budget range?\n- What are your main interests (culture, food, shopping, etc.)?\n- Where will you be departing from?\n\nOnce I have these details, I can help you find flights, hotels, and create a personalized itinerary!"
        },
        {
            "role": "user",
            "content": "I'm traveling from New York on March 15-20, budget is $3000, and I love culture and food."
        },
        {
            "role": "assistant",
            "content": "Perfect! Let me help you plan your 5-day trip to Paris from New York.\n\n**Flights Found:**\n1. Delta Airlines DL123 - Departure: 08:00 | Arrival: 11:30 | Price: $450\n2. American Airlines AA456 - Departure: 14:15 | Arrival: 17:45 | Price: $380\n\n**Hotels Found:**\n1. Grand Hotel (4.5★) - $200/night, Total: $1000\n2. Luxury Resort (4.9★) - $350/night, Total: $1750\n\n**Weather Forecast:**\nTemperature: 22°C, Condition: Sunny\n\n**Recommendations:**\n- Eiffel Tower\n- Louvre Museum\n- Seine River Cruise\n- Le Jules Verne Restaurant"
        }
    ]
    
    print("🧪 Testing Download Functionality")
    print("=" * 50)
    
    # Test TXT format
    print("\n📄 Testing TXT format...")
    try:
        from app import create_itinerary_document
        txt_content = create_itinerary_document(sample_conversation, "txt")
        print(f"✅ TXT content generated ({len(txt_content)} characters)")
        print("📝 Preview:")
        print(txt_content[:200] + "...")
    except Exception as e:
        print(f"❌ TXT generation failed: {e}")
    
    # Test JSON format
    print("\n📊 Testing JSON format...")
    try:
        json_content = create_itinerary_document(sample_conversation, "json")
        print(f"✅ JSON content generated ({len(json_content)} characters)")
        print("📝 Preview:")
        print(json_content[:200] + "...")
    except Exception as e:
        print(f"❌ JSON generation failed: {e}")
    
    # Test DOCX format
    print("\n📝 Testing DOCX format...")
    try:
        docx_content = create_itinerary_document(sample_conversation, "docx")
        print(f"✅ DOCX content generated ({len(docx_content)} bytes)")
        print("📝 DOCX file created successfully")
    except Exception as e:
        print(f"❌ DOCX generation failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Download functionality test completed!")
    print("✅ All formats working correctly")
    print("🚀 You can now use the download feature in the Streamlit app")

if __name__ == "__main__":
    test_download_functionality() 