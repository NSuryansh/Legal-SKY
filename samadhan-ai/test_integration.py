#!/usr/bin/env python3
"""
Integration Test Script
Tests the complete flow: Frontend -> Backend -> Sarvam AI -> Backend -> Frontend

This proves the backend is perfectly connected to 01_Sarvam_Gateway
"""

import requests
import base64
import io
import json
from gtts import gTTS

print("=" * 70)
print("🧪 SAMADHAN AI - INTEGRATION TEST")
print("=" * 70)
print("Testing: Frontend -> Backend -> Sarvam AI -> Response")
print("=" * 70)

# Configuration
BACKEND_URL = "http://localhost:8000"
TEST_LANGUAGE = "hi-IN"
TEST_TEXT = "मेरा नाम रमेश है और मुझे कानूनी सहायता चाहिए"

def test_health_check():
    """Test 1: Check if backend is running"""
    print("\n📋 TEST 1: Health Check")
    print("-" * 70)
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data['status']}")
            print(f"✅ Mode: {data['mode']}")
            print(f"✅ API Key Configured: {data['api_key_configured']}")
            print(f"✅ Integration: {data['integration']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure backend is running: uvicorn main:app --reload")
        return False

def test_audio_processing():
    """Test 2: Send real audio and get translation"""
    print("\n📋 TEST 2: Audio Processing (End-to-End)")
    print("-" * 70)
    
    try:
        # Step 1: Generate test audio (simulates frontend recording)
        print(f"🎙️  Generating test audio: \"{TEST_TEXT}\"")
        tts = gTTS(text=TEST_TEXT, lang='hi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Step 2: Convert to base64 (simulates frontend conversion)
        base64_audio = base64.b64encode(fp.read()).decode('utf-8')
        print(f"✅ Audio converted to base64 ({len(base64_audio)} characters)")
        
        # Step 3: Send POST request (simulates frontend API call)
        print(f"\n📡 Sending POST request to {BACKEND_URL}/api/process-audio")
        payload = {
            "audio_data": base64_audio,
            "language_code": TEST_LANGUAGE
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/process-audio",
            json=payload,
            timeout=30  # Sarvam AI can take some time
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS! Backend Response:")
            print("-" * 70)
            print(f"Status: {result['status']}")
            print(f"\n📝 Regional Input (Transcribed):")
            print(f"   {result['regional_input']}")
            print(f"\n🌎 English Query (Translated):")
            print(f"   {result['english_query']}")
            
            if 'message' in result:
                print(f"\n💬 Message: {result['message']}")
            
            print("-" * 70)
            
            # Verify it's not demo mode (unless API key missing)
            if result['status'] == 'success':
                print("\n🎉 REAL TRANSLATION WORKING! ✅")
                print("The backend is successfully connected to Sarvam AI!")
                return True
            elif result['status'] == 'demo_mode':
                print("\n⚠️  Running in demo mode (API key not loaded)")
                print("Check that .env file exists with SARVAM_API_KEY")
                return False
        else:
            print(f"\n❌ Request failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n❌ Request timeout - Sarvam AI might be slow")
        print("Try again or check your internet connection")
        return False
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n🚀 Starting integration tests...\n")
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n❌ Backend not running. Aborting tests.")
        return False
    
    # Test 2: Audio Processing
    if not test_audio_processing():
        print("\n❌ Audio processing test failed.")
        return False
    
    # All tests passed
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\n🎯 Your backend is perfectly connected to 01_Sarvam_Gateway")
    print("🚀 You can now run the frontend and start recording!")
    print("\nNext steps:")
    print("  1. Terminal 1: cd backend && uvicorn main:app --reload")
    print("  2. Terminal 2: cd frontend && npm run dev")
    print("  3. Open: http://localhost:5173")
    print("=" * 70)
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        exit(1)
