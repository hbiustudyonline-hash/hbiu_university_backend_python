#!/usr/bin/env python3
"""
AI Test Script for HBIU University Backend
Test various AI endpoints and functionalities
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8001"

def login_user(username: str, password: str) -> Dict[str, Any]:
    """Login and get authentication token"""
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return {}

def test_ai_capabilities(token: str) -> None:
    """Test AI capabilities endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/api/ai/capabilities", headers=headers)
    if response.status_code == 200:
        print("✅ AI Capabilities:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ AI Capabilities failed: {response.status_code} - {response.text}")

def test_study_assistant(token: str) -> None:
    """Test study assistant endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    
    test_data = {
        "question": "What is the difference between supervised and unsupervised learning?",
        "context": "Machine Learning course - Introduction to AI",
        "course_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/study-assistant", json=test_data, headers=headers)
    if response.status_code == 200:
        print("✅ Study Assistant Response:")
        result = response.json()
        print(f"Content: {result['content'][:200]}...")
        print(f"Success: {result['success']}")
    else:
        print(f"❌ Study Assistant failed: {response.status_code} - {response.text}")

def test_content_generation(token: str) -> None:
    """Test content generation endpoint (lecturer/admin only)"""
    headers = {"Authorization": f"Bearer {token}"}
    
    test_data = {
        "prompt": "Create a lesson about Python functions and their parameters",
        "content_type": "lesson",
        "subject": "Computer Science",
        "difficulty": "beginner",
        "length": "medium"
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/generate-content", json=test_data, headers=headers)
    if response.status_code == 200:
        print("✅ Content Generation Response:")
        result = response.json()
        print(f"Content: {result['content'][:200]}...")
        print(f"Success: {result['success']}")
        print(f"Metadata: {result['metadata']}")
    else:
        print(f"❌ Content Generation failed: {response.status_code} - {response.text}")

def test_quiz_generation(token: str) -> None:
    """Test quiz generation endpoint (lecturer/admin only)"""
    headers = {"Authorization": f"Bearer {token}"}
    
    test_data = {
        "topic": "Python Basic Syntax",
        "num_questions": 3,
        "difficulty": "beginner",
        "question_types": ["multiple_choice", "true_false"]
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/generate-quiz", json=test_data, headers=headers)
    if response.status_code == 200:
        print("✅ Quiz Generation Response:")
        result = response.json()
        print(f"Success: {result['success']}")
        if isinstance(result['content'], dict):
            print(f"Quiz Title: {result['content'].get('quiz_title', 'N/A')}")
            questions = result['content'].get('questions', [])
            print(f"Number of questions: {len(questions)}")
        print(f"Metadata: {result['metadata']}")
    else:
        print(f"❌ Quiz Generation failed: {response.status_code} - {response.text}")

def test_concept_explanation(token: str) -> None:
    """Test concept explanation endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    
    test_data = {
        "concept": "Object-Oriented Programming",
        "subject": "Computer Science",
        "level": "intermediate"
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/explain-concept", json=test_data, headers=headers)
    if response.status_code == 200:
        print("✅ Concept Explanation Response:")
        result = response.json()
        print(f"Content: {result['content'][:200]}...")
        print(f"Success: {result['success']}")
    else:
        print(f"❌ Concept Explanation failed: {response.status_code} - {response.text}")

def main():
    """Run all AI tests"""
    print("🚀 Starting AI functionality tests for HBIU University Backend\n")
    
    # Test with different user roles
    test_users = [
        ("student1", "student123", "Student"),
        ("lecturer1", "lecturer123", "Lecturer"),
        ("admin", "admin123", "Admin")
    ]
    
    for username, password, role in test_users:
        print(f"\n{'='*50}")
        print(f"Testing with {role} account: {username}")
        print(f"{'='*50}")
        
        # Login
        login_result = login_user(username, password)
        if not login_result:
            continue
            
        token = login_result.get("access_token")
        if not token:
            print("❌ No access token received")
            continue
            
        # Test AI capabilities
        test_ai_capabilities(token)
        print()
        
        # Test study assistant (available to all users)
        test_study_assistant(token)
        print()
        
        # Test concept explanation (available to all users)
        test_concept_explanation(token)
        print()
        
        # Test content generation (lecturer/admin only)
        if role in ["Lecturer", "Admin"]:
            test_content_generation(token)
            print()
            
            # Test quiz generation (lecturer/admin only)
            test_quiz_generation(token)
            print()
        
        print(f"✅ Completed tests for {role}")

if __name__ == "__main__":
    try:
        main()
        print("\n🎉 AI functionality tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the backend server. Make sure it's running on http://localhost:8001")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")