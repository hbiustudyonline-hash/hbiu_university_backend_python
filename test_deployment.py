#!/usr/bin/env python3
"""
Simple deployment test script to verify the backend is working correctly
"""

import requests
import json
import sys

def test_deployment(base_url="http://localhost:8000"):
    """Test basic functionality of the deployed backend"""
    
    print(f"🧪 Testing HBIU Python Backend at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health Check
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Health Check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health Check: ERROR - {e}")
        return False
    
    # Test 2: Authentication
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Authentication: PASSED")
            token_data = response.json()
            token = token_data.get("access_token")
            print(f"   User: {token_data['user']['username']} ({token_data['user']['role']})")
        else:
            print(f"❌ Authentication: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Authentication: ERROR - {e}")
        return False
    
    # Test 3: AI Capabilities
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/api/ai/capabilities", headers=headers)
        if response.status_code == 200:
            print("✅ AI Capabilities: PASSED")
            capabilities = response.json()
            print(f"   AI Service Available: {capabilities['ai_service_available']}")
            print(f"   User Role: {capabilities['user_role']}")
            print(f"   Available Features: {len(capabilities['capabilities'])}")
        else:
            print(f"❌ AI Capabilities: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ AI Capabilities: ERROR - {e}")
        return False
    
    # Test 4: API Documentation
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API Documentation: PASSED")
            print(f"   Swagger UI available at: {base_url}/docs")
        else:
            print(f"❌ API Documentation: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ API Documentation: ERROR - {e}")
    
    print("=" * 50)
    print("🎉 Deployment test completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Deploy to Railway using the provided guide")
    print("2. Set environment variables in Railway dashboard")
    print("3. Update frontend to use Railway URL")
    print("4. Test AI features with OpenAI API key")
    
    return True

if __name__ == "__main__":
    # Allow custom URL for testing Railway deployment
    test_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print("🚀 HBIU Backend Deployment Test")
    print(f"Testing URL: {test_url}")
    print()
    
    try:
        success = test_deployment(test_url)
        if not success:
            print("\n❌ Some tests failed. Check the output above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)