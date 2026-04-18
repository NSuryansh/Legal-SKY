"""
Samadhan AI - Complete Legal-SKY Integration
WITH AUTOMATIC LANGUAGE DETECTION + RAG PIPELINE
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import base64
import os
import sys
from typing import Optional, List, Dict, Any
import uvicorn

# Import Legal-SKY wrapper from local modules directory
try:
    from modules.legal_wrapper import handle_user_query
    LEGAL_SKY_AVAILABLE = True
    print("✅ Legal-SKY modules loaded successfully")
except ImportError as e:
    LEGAL_SKY_AVAILABLE = False
    print(f"⚠️  Legal-SKY modules not available: {e}")
    handle_user_query = None

app = FastAPI(
    title="Samadhan AI",
    description="Sovereign AI Portal with Auto Language Detection + Legal RAG",
    version="4.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SARVAM_KEY = os.getenv("SARVAM_API_KEY", "")

# =============================================================================
# AUTOMATIC LANGUAGE DETECTION + PROCESSING
# =============================================================================

def auto_detect_and_process(base64_audio_string):
    """
    Auto-detects language and processes audio in one step
    Uses Sarvam AI's multi-lingual ASR (no language_code needed!)
    """
    print("🎙️ Processing audio with AUTO-DETECTION...")
    
    asr_endpoint = "https://api.sarvam.ai/speech-to-text"
    asr_headers = {"api-subscription-key": SARVAM_KEY}
    
    try:
        # Decode audio
        audio_bytes = base64.b64decode(base64_audio_string)
        files = {'file': ('audio.wav', audio_bytes, 'audio/wav')}
        
        # ASR WITHOUT language_code = Auto-detection!
        data = {}  # Empty = auto-detect
        
        asr_response = requests.post(asr_endpoint, headers=asr_headers, files=files, data=data, timeout=30)
        asr_response.raise_for_status()
        
        asr_result = asr_response.json()
        regional_transcript = asr_result.get('transcript', '')
        detected_language = asr_result.get('language_code', 'hi-IN')  # Sarvam returns detected language
        
        print(f"✅ Detected Language: {detected_language}")
        print(f"✅ Transcribed: {regional_transcript}")
        
        # Translate to English
        translate_endpoint = "https://api.sarvam.ai/translate"
        trans_headers = {"api-subscription-key": SARVAM_KEY, "Content-Type": "application/json"}
        trans_payload = {
            "input": regional_transcript,
            "source_language_code": detected_language,
            "target_language_code": "en-IN",
            "speaker_gender": "Male",
            "mode": "formal"
        }
        
        trans_response = requests.post(translate_endpoint, headers=trans_headers, json=trans_payload, timeout=30)
        trans_response.raise_for_status()
        english_query = trans_response.json()['translated_text']
        
        print(f"✅ Translated: {english_query}")
        
        return {
            "success": True,
            "status": "success",
            "detected_language": detected_language,
            "regional_input": regional_transcript,
            "english_query": english_query
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "success": False,
            "status": "error",
            "error": str(e),
            "message": str(e)
        }

def translate_rag_output(english_text, target_language="hi-IN"):
    """Translate English back to regional language"""
    if not SARVAM_KEY:
        return english_text
    
    endpoint = "https://api.sarvam.ai/translate"
    headers = {"api-subscription-key": SARVAM_KEY, "Content-Type": "application/json"}
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
        return english_text

# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class AudioProcessRequest(BaseModel):
    audio_data: str

class SourceDocument(BaseModel):
    chunk_id: Optional[str] = None
    title: Optional[str] = None
    page: Optional[int] = None
    source_file: Optional[str] = None
    text: Optional[str] = None
    score: Optional[float] = None

class LegalQueryResponse(BaseModel):
    success: bool
    status: str
    detected_language: Optional[str] = None
    regional_input: str
    english_query: str
    legal_answer: str
    intents: List[str]
    intent_scores: Optional[Dict[str, float]] = None
    sources: List[Dict[str, Any]]
    action_pack: Optional[str] = None
    error: Optional[str] = None
    message: Optional[str] = None

class AudioProcessResponse(BaseModel):
    success: bool
    status: str
    detected_language: Optional[str] = None
    regional_input: str
    english_query: str
    error: Optional[str] = None
    message: Optional[str] = None

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Samadhan AI - Complete Legal-SKY Integration",
        "version": "4.1.0",
        "sarvam_configured": bool(SARVAM_KEY),
        "legal_sky_available": LEGAL_SKY_AVAILABLE,
        "features": [
            "Auto Language Detection",
            "9 Indian Languages",
            "Real-time Translation",
            "Legal RAG Pipeline",
            "Intent Classification",
            "Source Citations",
            "Citizen Action Packs"
        ]
    }

@app.post("/api/process-audio", response_model=AudioProcessResponse)
async def process_audio(request: AudioProcessRequest):
    """
    Simple audio processing without legal RAG
    For backward compatibility
    """
    try:
        if not request.audio_data:
            raise HTTPException(status_code=400, detail="No audio data")
        
        if not SARVAM_KEY:
            # Demo mode
            return AudioProcessResponse(
                success=False,
                status="demo_mode",
                detected_language="hi-IN",
                regional_input="मेरा नाम रमेश है",
                english_query="My name is Ramesh",
                message="Demo mode - no API key"
            )
        
        # Auto-detect and process
        result = auto_detect_and_process(request.audio_data)
        
        if not result.get("success"):
            return AudioProcessResponse(
                success=False,
                status="error",
                regional_input="",
                english_query="",
                error=result.get("error", "Unknown error"),
                message=result.get("message", "Processing failed")
            )
        
        return AudioProcessResponse(
            success=True,
            status=result["status"],
            detected_language=result.get("detected_language"),
            regional_input=result["regional_input"],
            english_query=result["english_query"]
        )
    except HTTPException:
        raise
    except Exception as e:
        return AudioProcessResponse(
            success=False,
            status="error",
            regional_input="",
            english_query="",
            error=str(e),
            message="Server error"
        )

@app.post("/api/legal-query", response_model=LegalQueryResponse)
async def legal_query(request: AudioProcessRequest):
    """
    COMPLETE LEGAL PIPELINE:
    1. Auto-detect language from audio
    2. Transcribe to text
    3. Translate to English
    4. Run Legal-SKY RAG pipeline
    5. Translate answer back to original language
    6. Return with intents, sources, action pack
    """
    try:
        if not request.audio_data:
            raise HTTPException(status_code=400, detail="No audio data")
        
        if not SARVAM_KEY:
            return LegalQueryResponse(
                success=False,
                status="error",
                regional_input="",
                english_query="",
                legal_answer="",
                intents=[],
                sources=[],
                message="Sarvam API key not configured"
            )
        
        if not LEGAL_SKY_AVAILABLE:
            return LegalQueryResponse(
                success=False,
                status="error",
                regional_input="",
                english_query="",
                legal_answer="",
                intents=[],
                sources=[],
                message="Legal-SKY modules not available"
            )
        
        # Step 1: Auto-detect and process audio
        print("\n" + "="*70)
        print("🎯 LEGAL QUERY PROCESSING PIPELINE")
        print("="*70)
        
        asr_result = auto_detect_and_process(request.audio_data)
        
        if not asr_result.get("success"):
            return LegalQueryResponse(
                success=False,
                status="error",
                regional_input="",
                english_query="",
                legal_answer="",
                intents=[],
                sources=[],
                error=asr_result.get("error", "Unknown error"),
                message="Audio processing failed"
            )
        
        detected_language = asr_result["detected_language"]
        regional_input = asr_result["regional_input"]
        english_query = asr_result["english_query"]
        
        # Step 2: Run Legal-SKY pipeline
        print(f"\n🔍 Running Legal-SKY pipeline for: {english_query}")
        
        try:
            legal_result = handle_user_query(english_query, detected_language)
        except Exception as e:
            print(f"❌ Legal-SKY pipeline error: {e}")
            import traceback
            traceback.print_exc()
            
            # Return a graceful fallback
            return LegalQueryResponse(
                success=False,
                status="error",
                detected_language=detected_language,
                regional_input=regional_input,
                english_query=english_query,
                legal_answer="",
                intents=[],
                sources=[],
                error=str(e),
                message=f"Legal processing temporarily unavailable: {str(e)}"
            )
        
        if legal_result["status"] != "success":
            return LegalQueryResponse(
                success=False,
                status="error",
                detected_language=detected_language,
                regional_input=regional_input,
                english_query=english_query,
                legal_answer="",
                intents=[],
                sources=[],
                error=legal_result.get("message", "Legal processing failed")
            )
        
        # Return complete result
        return LegalQueryResponse(
            success=True,
            status="success",
            detected_language=detected_language,
            regional_input=regional_input,
            english_query=english_query,
            legal_answer=legal_result["final_answer"],
            intents=legal_result["intents"],
            intent_scores=legal_result.get("intent_scores"),
            sources=legal_result.get("sources", []),
            action_pack=legal_result.get("action_pack"),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        return LegalQueryResponse(
            success=False,
            status="error",
            regional_input="",
            english_query="",
            legal_answer="",
            intents=[],
            sources=[],
            error=str(e),
            message="Server error during legal query processing"
        )

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/dist/index.html")

if __name__ == "__main__":
    print("="*70)
    print("🚀 SAMADHAN AI v4.1 - COMPLETE LEGAL-SKY INTEGRATION")
    print("="*70)
    print(f"✅ Port: 8000")
    print(f"✅ Sarvam AI: {'Configured' if SARVAM_KEY else 'Missing'}")
    print(f"✅ Legal-SKY: {'Available' if LEGAL_SKY_AVAILABLE else 'Not Available'}")
    print(f"✅ Features:")
    print(f"   - Auto Language Detection (9 languages)")
    print(f"   - Intent Classification")
    print(f"   - RAG Pipeline with Vector Search")
    print(f"   - Source Citations")
    print(f"   - Citizen Action Packs")
    print("="*70)
    uvicorn.run(app, host="0.0.0.0", port=8000)
