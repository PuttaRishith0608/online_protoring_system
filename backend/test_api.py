"""
Test script to verify the backend API is working correctly
Run this after starting the backend server

Usage:
    python test_api.py
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print(f"{'='*60}")
    print(json.dumps(response.json(), indent=2))


def test_health():
    """Test health check endpoint"""
    print("\n🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)


def test_log_events():
    """Test logging various events"""
    print("\n🔍 Testing event logging...")
    
    user_id = "test_user_001"
    events = [
        {
            "user_id": user_id,
            "event_type": "copy_paste",
            "timestamp": time.time(),
            "metadata": {"source": "exam_text", "destination": "answer_field"}
        },
        {
            "user_id": user_id,
            "event_type": "tab_switch",
            "timestamp": time.time(),
            "metadata": {"new_tab": "google.com", "switching_from": "exam"}
        },
        {
            "user_id": user_id,
            "event_type": "answer_submission",
            "timestamp": time.time(),
            "metadata": {
                "answer": "This is a suspiciously long answer that is definitely over 200 characters long. " * 3,
                "time_taken_seconds": 5,
                "question_id": "q1"
            }
        },
        {
            "user_id": user_id,
            "event_type": "copy_paste",
            "timestamp": time.time(),
            "metadata": {"source": "stackoverflow", "destination": "answer_field"}
        },
        {
            "user_id": user_id,
            "event_type": "tab_switch",
            "timestamp": time.time(),
            "metadata": {"new_tab": "discord.com"}
        },
    ]
    
    for i, event in enumerate(events):
        response = requests.post(f"{BASE_URL}/log-event", json=event)
        print(f"  [{i+1}] {event['event_type']} - {response.status_code}")


def test_get_events():
    """Test retrieving all events for a user"""
    print("\n🔍 Testing event retrieval...")
    
    user_id = "test_user_001"
    response = requests.get(f"{BASE_URL}/events/{user_id}")
    print_response(f"All Events for {user_id}", response)


def test_get_report():
    """Test getting integrity report"""
    print("\n🔍 Testing integrity report...")
    
    user_id = "test_user_001"
    response = requests.get(f"{BASE_URL}/report/{user_id}")
    
    if response.status_code == 200:
        report = response.json()
        print_response(f"Integrity Report for {user_id}", response)
        
        # Analyze the report
        print(f"\n📊 Analysis:")
        print(f"   - Copy-Paste Events: {report['copy_paste_count']}")
        print(f"   - Tab Switches: {report['tab_switch_count']}")
        print(f"   - AI Suspicions: {report['ai_suspicion_count']}")
        print(f"   - Integrity Score: {report['integrity_score']}")
        
        if report['details']['suspicious_answers']:
            print(f"\n🚨 Suspicious Answers Detected:")
            for ans in report['details']['suspicious_answers']:
                print(f"   - {ans['reason']} (Length: {ans['answer_length']}, Time: {ans['time_taken']}s)")


def test_clean_user():
    """Test with a clean user (no violations)"""
    print("\n🔍 Testing clean user (no violations)...")
    
    user_id = "clean_user_001"
    
    # Log only legitimate events (no copy-paste, normal tab switches, long answer with plenty of time)
    clean_events = [
        {
            "user_id": user_id,
            "event_type": "answer_submission",
            "timestamp": time.time(),
            "metadata": {
                "answer": "This is a legitimate answer that takes proper time to write.",
                "time_taken_seconds": 120,  # 2 minutes - plenty of time
                "question_id": "q1"
            }
        },
    ]
    
    for event in clean_events:
        requests.post(f"{BASE_URL}/log-event", json=event)
    
    # Get report
    response = requests.get(f"{BASE_URL}/report/{user_id}")
    if response.status_code == 200:
        report = response.json()
        print(f"\n📊 Clean User Report:")
        print(f"   - Integrity Score: {report['integrity_score']} ✅")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 Online Proctoring System - API Test Suite")
    print("="*60)
    
    try:
        test_health()
        test_log_events()
        test_get_events()
        test_get_report()
        test_clean_user()
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)
        print("\n📚 API Documentation available at: http://localhost:8000/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to backend server")
        print("   Make sure the backend is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
