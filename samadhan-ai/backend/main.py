from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Samadhan AI Backend - Connected to 01_Sarvam_Gateway",
    description="Real-time Translation Gateway using Sarvam AI",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Sarvam API Key from .env file
SARVAM_KEY = os.getenv("SARVAM_API_KEY")

if not SARVAM_KEY:
    print("⚠️  WARNING: SARVAM_API_KEY not found in .env file. Running in demo mode.")
else:
    print(f"✅ Sarvam API Key loaded: {SARVAM_KEY[:10]}...")

class AudioProcessRequest(BaseModel):
    audio_data: str  # Base64 encoded audio
    language_code: str  # e.g., "hi-IN"

class AudioProcessResponse(BaseModel):
    status: str
    regional_input: str
    english_query: str
    message: Optional[str] = None

# ============================================================================
# EXACT COPY FROM 01_Sarvam_Gateway NOTEBOOK - Cell 1
# This is the SAME function that runs in the notebook
# ============================================================================

def process_audio_query(base64_audio_string, language_code="hi-IN"):
    """
    Step 1: Converts Regional Audio to Regional Text (ASR)
    Step 2: Translates Regional Text to English for the RAG Vector DB
    
    THIS IS THE EXACT SAME FUNCTION FROM THE NOTEBOOK!
    """
    print(f"🎙️ Processing incoming audio ({language_code})...")
    
    # 1. Speech-to-Text (ASR)
    asr_endpoint = "https://api.sarvam.ai/speech-to-text"
    
    # CRITICAL FIX: Do NOT set "Content-Type: application/json" here.
    # The requests library will automatically set multipart/form-data when using 'files'
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
    EXACT COPY FROM NOTEBOOK!
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
        return f"Translation failed: {str(e)}"

# ============================================================================
# FASTAPI ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Samadhan AI Backend - CONNECTED to 01_Sarvam_Gateway",
        "version": "2.0.0",
        "notebook": "01_Sarvam_Gateway",
        "sarvam_configured": bool(SARVAM_KEY),
        "status": "ready" if SARVAM_KEY else "demo_mode"
    }

@app.post("/api/process-audio", response_model=AudioProcessResponse)
async def process_audio(request: AudioProcessRequest):
    """
    Process audio using the EXACT same function from the notebook.
    This ensures 100% compatibility with your tested code.
    """
    try:
        # Validate input
        if not request.audio_data:
            raise HTTPException(status_code=400, detail="No audio data provided")
        
        if not SARVAM_KEY:
            # Fallback to demo mode
            print("⚠️ Running in DEMO MODE - API key not configured")
            language_examples = {
                "hi-IN": ("मेरा नाम रमेश है और मुझे कानूनी सहायता चाहिए", 
                         "My name is Ramesh and I need legal assistance"),
                "bn-IN": ("আমার নাম রমেশ এবং আমার আইনি সহায়তা প্রয়োজন",
                         "My name is Ramesh and I need legal assistance"),
                "te-IN": ("నా పేరు రమేష్ మరియు నాకు చట్టపరమైన సహాయం అవసరం",
                         "My name is Ramesh and I need legal assistance"),
            }
            regional_text, english_text = language_examples.get(
                request.language_code, 
                language_examples["hi-IN"]
            )
            
            return AudioProcessResponse(
                status="demo_mode",
                regional_input=regional_text,
                english_query=english_text,
                message="Demo mode: Set SARVAM_API_KEY in .env to enable real translation."
            )
        
        # ====================================================================
        # CALL THE EXACT SAME FUNCTION FROM THE NOTEBOOK
        # ====================================================================
        print(f"🚀 Processing with 01_Sarvam_Gateway function...")
        result = process_audio_query(
            base64_audio_string=request.audio_data,
            language_code=request.language_code
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Sarvam API Error",
                    "message": result.get("message"),
                    "hint": "Check backend logs for details"
                }
            )
        
        return AudioProcessResponse(
            status=result["status"],
            regional_input=result["regional_input"],
            english_query=result["english_query"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_message = str(e)
        print(f"❌ Error: {error_message}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Processing failed",
                "message": error_message
            }
        )

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Samadhan AI Backend",
        "version": "2.0.0",
        "integration": "01_Sarvam_Gateway (Direct Connection)",
        "api_key_configured": bool(SARVAM_KEY),
        "mode": "LIVE" if SARVAM_KEY else "DEMO",
        "endpoints": {
            "process_audio": "/api/process-audio",
            "health": "/api/health",
            "root": "/"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("="*70)
    print("🚀 SAMADHAN AI BACKEND - CONNECTED TO 01_SARVAM_GATEWAY")
    print("="*70)
    print(f"📡 Sarvam API Key: {'✅ Loaded' if SARVAM_KEY else '❌ Not Found'}")
    print(f"🔧 Mode: {'LIVE (Real Translation)' if SARVAM_KEY else 'DEMO (Sample Data)'}")
    print("="*70)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)