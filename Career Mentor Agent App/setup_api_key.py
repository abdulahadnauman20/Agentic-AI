#!/usr/bin/env python3
"""
Setup script to help configure Gemini API key for Career Mentor Agent
"""

import os
import sys

def create_env_file():
    """Create .env file with API key."""
    print("🔑 Gemini API Key Setup")
    print("=" * 40)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📋 Steps to get your API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Get API key' or 'Create API key'")
    print("4. Copy the generated key (starts with 'AIza...')")
    print("5. Paste it below\n")
    
    # Get API key from user
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    if not api_key.startswith('AIza'):
        print("⚠️  Warning: API key doesn't start with 'AIza'. Are you sure this is correct?")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Create .env file
    try:
        with open('.env', 'w') as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        
        print("✅ .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return
    
    # Test the API key
    print("\n🧪 Testing API key...")
    test_api_key(api_key)

def test_api_key(api_key):
    """Test if the API key works."""
    try:
        # Set environment variable
        os.environ['GEMINI_API_KEY'] = api_key
        
        # Import and test
        import config
        from gemini_client import GeminiClient
        
        # Test client initialization
        client = GeminiClient()
        print("✅ API key is valid!")
        
        # Test a simple request
        response = client.generate_response("Hello, test message")
        if "Error" not in response:
            print("✅ API connection successful!")
            print("🎉 Your Career Mentor Agent is ready to use!")
        else:
            print("⚠️  API key works but there might be an issue with the model")
            
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        print("Please check your API key and try again.")

def main():
    """Main setup function."""
    print("🚀 Career Mentor Agent - API Key Setup")
    print("=" * 50)
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("📁 .env file found!")
        with open('.env', 'r') as f:
            content = f.read()
            if 'GEMINI_API_KEY' in content:
                print("✅ API key is already configured!")
                response = input("Do you want to update it? (y/n): ")
                if response.lower() == 'y':
                    create_env_file()
                else:
                    print("Setup completed.")
                    return
            else:
                print("⚠️  .env file exists but no API key found.")
                create_env_file()
    else:
        print("📁 No .env file found. Creating new one...")
        create_env_file()
    
    print("\n📖 Next steps:")
    print("1. Run: python test_app.py")
    print("2. Run: streamlit run app.py")
    print("3. Open: http://localhost:8501")

if __name__ == "__main__":
    main() 