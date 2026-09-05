#!/usr/bin/env python3
import sys

def test_app_import():
    print("Testing Streamlit app import...")
    
    try:
        import app
        print("✓ Successfully imported app module")
        return True
    except Exception as e:
        print(f"✗ Failed to import app module: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_app_import()
    sys.exit(0 if success else 1)