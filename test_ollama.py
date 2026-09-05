#!/usr/bin/env python3
import sys
import requests
import json
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL

def test_ollama_connection():
    print("Testing Ollama connection...")
    
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"✓ Ollama server is running at {OLLAMA_BASE_URL}")
        else:
            print(f"✗ Ollama server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to Ollama server at {OLLAMA_BASE_URL}")
        print("Please ensure Ollama is installed and running:")
        print("  brew install ollama")
        print("  ollama serve")
        return False
    except Exception as e:
        print(f"✗ Error connecting to Ollama: {str(e)}")
        return False
    
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        data = response.json()
        models = [model['name'] for model in data.get('models', [])]
        
        print(f"\nAvailable models: {len(models)}")
        for model in models:
            print(f"  - {model}")
        
        if OLLAMA_MODEL in models:
            print(f"\n✓ Required model '{OLLAMA_MODEL}' is available")
        else:
            print(f"\n✗ Required model '{OLLAMA_MODEL}' is not available")
            print(f"Please pull the model:")
            print(f"  ollama pull {OLLAMA_MODEL}")
            return False
            
    except Exception as e:
        print(f"Error checking models: {str(e)}")
        return False
    
    print(f"\nTesting inference with {OLLAMA_MODEL}...")
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": "Hello, this is a test.",
            "stream": False
        }
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'response' in result:
                print(f"✓ Model inference successful")
                print(f"  Response: {result['response'][:100]}...")
                return True
            else:
                print(f"✗ Unexpected response format")
                return False
        else:
            print(f"✗ Inference failed with status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error during inference: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_ollama_connection()
    sys.exit(0 if success else 1)