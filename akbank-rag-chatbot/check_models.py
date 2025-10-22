#!/usr/bin/env python3
"""
Script to check available Google Gemini models
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables")
    exit(1)

print("Checking available Google Gemini models...")
print("=" * 50)

try:
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    headers = {"x-goog-api-key": GEMINI_API_KEY}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("Available models that support generateContent:")
        print()
        
        for model in data.get("models", []):
            name = model.get("name", "")
            display_name = model.get("displayName", "")
            methods = model.get("supportedGenerationMethods", [])
            
            if "generateContent" in methods:
                print(f"✅ Model: {name}")
                print(f"   Display Name: {display_name}")
                print(f"   Methods: {methods}")
                print()
                
        print("\nFor LangChain, use these model names:")
        for model in data.get("models", []):
            name = model.get("name", "")
            methods = model.get("supportedGenerationMethods", [])
            if "generateContent" in methods:
                # Remove 'models/' prefix for LangChain
                clean_name = name.replace("models/", "")
                print(f"   {clean_name}")
                
    else:
        print(f"API request failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
    print("Make sure your GEMINI_API_KEY is correct and you have internet access.")