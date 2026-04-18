"""
Sarvam AI Translation Module
Extracted from: 01_Sarvam_Gateway notebook
Provides audio transcription and text translation for Indian languages
"""

import requests
import base64
import os

# Get API key from environment (set in app.yaml)
SARVAM_KEY = os.getenv("SARVAM_API_KEY", "sk_sn9w8roe_QwQ3Sc7Xa9acvNvTh5iV8Iek")


def process_audio_query(base64_audio_string, language_code="hi-IN"):
    """
    Step 1: Converts Regional Audio to Regional Text (ASR)
    Step 2: Translates Regional Text to English for the RAG Vector DB
    
    Args:
        base64_audio_string: Base64 encoded audio data
        language_code: Language code (e.g., "hi-IN", "bn-IN")
    
    Returns:
        dict with status, regional_input, english_query
    """
    print(f"🎙️ Processing incoming audio ({language_code})...")
    
    # 1. Speech-to-Text (ASR)
    asr_endpoint = "https://api.sarvam.ai/speech-to-text"
    asr_headers = {
        "api-subscription-key": SARVAM_KEY
    }
    
    try:
        # Decode the base64 string back into binary audio bytes
        audio_bytes = base64.b64decode(base64_audio_string)
        
        # Package it as a form-data file upload
        files = {
            'file': ('audio.wav', audio_bytes, 'audio/wav')
        }
        data = {
            'language_code': language_code
        }
        
        asr_response = requests.post(asr_endpoint, headers=asr_headers, files=files, data=data, timeout=30)
        asr_response.raise_for_status()
        regional_transcript = asr_response.json().get('transcript', '')
        
        print(f"✅ Transcribed: {regional_transcript}")
        
        # 2. Translate to English
        translate_endpoint = "https://api.sarvam.ai/translate"
        trans_headers = {
            "api-subscription-key": SARVAM_KEY,
            "Content-Type": "application/json"
        }
        trans_payload = {
            "input": regional_transcript,
            "source_language_code": language_code,
            "target_language_code": "en-IN",
            "speaker_gender": "Male",
            "mode": "formal"
        }
        
        trans_response = requests.post(translate_endpoint, headers=trans_headers, json=trans_payload, timeout=30)
        trans_response.raise_for_status()
        english_query = trans_response.json()['translated_text']
        
        print(f"✅ Translated for AI: {english_query}")
        
        return {
            "status": "success",
            "regional_input": regional_transcript,
            "english_query": english_query
        }
        
    except Exception as e:
        print(f"Pipeline Error: {e}")
        if 'asr_response' in locals(): 
            print(f"Sarvam API Response: {asr_response.text}")
        return {"status": "error", "message": str(e)}


def translate_rag_output(english_text, target_language="hi-IN"):
    """
    Translates the LLM's English legal advice back into the citizen's native language.
    
    Args:
        english_text: English text to translate
        target_language: Target language code (e.g., "hi-IN")
    
    Returns:
        Translated text string
    """
    endpoint = "https://api.sarvam.ai/translate"
    headers = {
        "api-subscription-key": SARVAM_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "input": english_text,
        "source_language_code": "en-IN",
        "target_language_code": target_language,
        "speaker_gender": "Male",
        "mode": "formal"
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['translated_text']
    except Exception as e:
        print(f"Translation failed: {e}")
        return f"Translation failed: {str(e)}"
