#!/usr/bin/env python3
"""
Setup script for AI Travel Agent
This script helps users set up the environment and dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    try:
        with open(".env", "w") as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("✅ .env file created successfully!")
        print("⚠️  Please edit .env file and add your actual OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_api_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print("✅ OpenAI API key is configured")
        return True
    else:
        print("⚠️  OpenAI API key not configured")
        print("Please set your OpenAI API key in the .env file")
        return False

def main():
    """Main setup function"""
    print("🚀 AI Travel Agent Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Check API key
    api_key_configured = check_api_key()
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed!")
    
    if api_key_configured:
        print("✅ You're ready to go!")
        print("🚀 Run 'streamlit run app.py' to start the application")
    else:
        print("⚠️  Please configure your OpenAI API key before running the app")
        print("📝 Edit the .env file and add your API key")
        print("🔑 Get your API key from: https://platform.openai.com/")
    
    print("\n📚 For more information, see README.md")
    
    return True

if __name__ == "__main__":
    main() 