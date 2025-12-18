#!/usr/bin/env python3
"""
Quick production test for HBIU Python Backend
Tests the Railway deployment at: hbiuuniversitybackendpython-production.up.railway.app
"""

import requests
import json

def test_production_deployment():
    """Test the production deployment on Railway"""
    
    base_url = "https://hbiuuniversitybackendpython-production.up.railway.app"
    print(f"🧪 Testing HBIU Python Backend Production Deployment")
    print(f"URL: {base_url}")
    print("=" * 70)
    
    # Test 1: Health Check
    try:
        print("1. Testing Health Check...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Health Check: PASSED")
            data = response.json()
            print(f"   📋 Status: {data.get('status', 'unknown')}")
            print(f"   📋 Message: {data.get('message', 'No message')}")
        else:
            print(f"   ❌ Health Check: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Health Check: ERROR - {e}")
        return False
    
    # Test 2: API Documentation
    try:
        print("\n2. Testing API Documentation...")
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("   ✅ API Documentation: ACCESSIBLE")
            print(f"   🔗 Swagger UI: {base_url}/docs")
        else:
            print(f"   ⚠️  API Documentation: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ API Documentation: ERROR - {e}")
    
    # Test 3: Authentication Endpoint
    try:
        print("\n3. Testing Authentication Endpoint...")
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            print("   ✅ Authentication: WORKING")
            token_data = response.json()
            print(f"   👤 User: {token_data.get('user', {}).get('username', 'unknown')}")
            print(f"   🔑 Role: {token_data.get('user', {}).get('role', 'unknown')}")
            
            # Test AI capabilities with token
            try:
                token = token_data.get("access_token")
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get(f"{base_url}/api/ai/capabilities", headers=headers, timeout=10)
                if response.status_code == 200:
                    print("   ✅ AI Capabilities: ACCESSIBLE")
                    ai_data = response.json()
                    print(f"   🤖 AI Service: {'Available' if ai_data.get('ai_service_available') else 'Unavailable'}")
                else:
                    print(f"   ⚠️  AI Capabilities: Status {response.status_code}")
            except Exception as e:
                print(f"   ❌ AI Capabilities: ERROR - {e}")
                
        else:
            print(f"   ❌ Authentication: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Authentication: ERROR - {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Production deployment test completed!")
    print(f"\n📋 Production URLs:")
    print(f"   🌐 API Base: {base_url}")
    print(f"   📚 Documentation: {base_url}/docs")
    print(f"   🔍 Health Check: {base_url}/")
    print(f"\n💡 Next Steps:")
    print("   1. Update frontend to use production API URL")
    print("   2. Test all AI features with OpenAI API key")
    print("   3. Monitor Railway deployment logs")
    
    return True

if __name__ == "__main__":
    try:
        test_production_deployment()
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")