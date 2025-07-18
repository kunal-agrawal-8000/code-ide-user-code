#!/usr/bin/env python3
"""
Simple test script for Twitter Clone functionality
"""

import requests
import json
import time

def test_twitter_clone():
    """Test basic Twitter Clone functionality"""
    base_url = "http://127.0.0.1:5000"
    
    print("Testing Twitter Clone functionality...")
    
    # Test 1: Check if app is running
    try:
        response = requests.get(base_url)
        print(f"✓ App is running - Status: {response.status_code}")
        
        # Should redirect to login page
        if response.url.endswith('/login'):
            print("✓ Redirects to login page when not authenticated")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ App is not running: {e}")
        return False
    
    # Test 2: Check registration page
    try:
        response = requests.get(f"{base_url}/register")
        if response.status_code == 200:
            print("✓ Registration page accessible")
        else:
            print(f"✗ Registration page error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Registration page error: {e}")
    
    # Test 3: Test API endpoint (should require authentication)
    try:
        response = requests.get(f"{base_url}/api/tweets")
        if response.status_code == 401:
            print("✓ API properly requires authentication")
        else:
            print(f"✗ API authentication check failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ API endpoint error: {e}")
    
    print("\nBasic functionality tests completed!")
    return True

if __name__ == "__main__":
    test_twitter_clone()