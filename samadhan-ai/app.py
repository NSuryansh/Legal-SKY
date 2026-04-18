"""
Legal-SKY AI Assistant - Complete Deployment
Multi-language Legal RAG System with Voice + Text Support
"""

import base64
import requests
import logging
import sys
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# =========================
# FIX: Add modules to path BEFORE importing
# =========================
current_dir = Path(__file__).parent
modules_dir = current_dir / "modules"
sys.path.insert(0, str(modules_dir))

# Import Legal-SKY modules
try:
    from legal_wrapper import handle_user_query
    from sarvam_translation import process_audio_query, translate_rag_output
    from intent_classifier import sementic_intent_classification
    from rag_pipeline import run_rag_pipeline
    LEGAL_SKY_AVAILABLE = True
    print("✅ Legal-SKY modules loaded successfully")
except Exception as e:
    LEGAL_SKY_AVAILABLE = False
    print(f"⚠️ Legal-SKY modules not available: {e}")

# =========================
# CONFIG
# =========================
SARVAM_KEY = os.getenv("SARVAM_API_KEY", "")

if not SARVAM_KEY:
    try:
        import yaml
        config_path = Path(__file__).parent / "app.yaml"
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
                env_vars = config.get("env", [])
                for env_var in env_vars:
                    if env_var.get("name") == "SARVAM_API_KEY":
                        SARVAM_KEY = env_var.get("value", "")
                        break
    except Exception:
        pass

SARVAM_ASR_ENDPOINT = "https://api.sarvam.ai/speech-to-text"
SARVAM_TRANSLATE_ENDPOINT = "https://api.sarvam.ai/translate"

# =========================
# LOGGER
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("legal-sky-app")

# =========================
# FASTAPI INIT
# =========================
app = FastAPI(
    title="Legal-SKY AI Assistant",
    description="Complete Legal RAG Assistant with Voice + Text Support",
    version="5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dist = Path(__file__).parent / "frontend" / "dist"
if frontend_dist.exists() and (frontend_dist / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

# =========================
# REQUEST MODELS
# =========================
class LegalQueryRequest(BaseModel):
    audio_data: Optional[str] = None
    query: Optional[str] = None
    language: Optional[str] = "en-IN"

# =========================
# RESPONSE MODELS
# =========================
class QueryResponse(BaseModel):
    success: bool
    status: str
    detected_language: Optional[str] = None
    regional_input: Optional[str] = None
    english_query: Optional[str] = None
    legal_answer: Optional[str] = None
    english_legal_answer: Optional[str] = None
    intents: Optional[List[str]] = None
    intent_scores: Optional[Dict[str, float]] = None
    sources: Optional[List[Dict]] = None
    action_pack: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None

# =========================
# HELPER FUNCTIONS
# =========================
def is_english_language(code: Optional[str]) -> bool:
    if not code:
        return False
    return code.lower().startswith("en")

def auto_detect_and_process(base64_audio: str):
    """Automatically detect language and transcribe audio"""
    try:
        audio_bytes = base64.b64decode(base64_audio)

        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        headers = {"api-subscription-key": SARVAM_KEY}

        response = requests.post(
            SARVAM_ASR_ENDPOINT,
            headers=headers,
            files=files,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        transcript = result.get("transcript", "").strip()
        language = result.get("language_code", "en-IN")

        if not transcript:
            raise ValueError("ASR returned empty transcript")

        logger.info(f"Detected language: {language}")
        logger.info(f"Transcript: {transcript}")
        return transcript, language

    except Exception as e:
        logger.error(f"ASR Error: {str(e)}")
        raise

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text using Sarvam"""
    if not text.strip():
        return text

    if source_lang == target_lang:
        return text

    try:
        headers = {
            "api-subscription-key": SARVAM_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "input": text,
            "source_language_code": source_lang,
            "target_language_code": target_lang,
            "mode": "formal"
        }

        response = requests.post(
            SARVAM_TRANSLATE_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        translated = response.json().get("translated_text")

        if not translated:
            raise ValueError("Translation returned empty text")

        return translated

    except Exception as e:
        logger.error(f"Translation Error ({source_lang} -> {target_lang}): {str(e)}")
        raise

def translate_to_english(text: str, source_lang: str) -> str:
    """Translate regional language to English"""
    if is_english_language(source_lang):
        return text
    return translate_text(text, source_lang, "en-IN")

def translate_from_english(text: str, target_lang: str) -> str:
    """Translate English text back to original language"""
    if is_english_language(target_lang):
        return text
    return translate_text(text, "en-IN", target_lang)

# =========================
# ENDPOINTS
# =========================
@app.get("/")
async def serve_frontend():
    index_file = frontend_dist / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))

    return {
        "service": "Legal-SKY AI Assistant",
        "version": "5.0",
        "status": "ready",
        "legal_sky_enabled": LEGAL_SKY_AVAILABLE,
        "api_configured": bool(SARVAM_KEY)
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Legal-SKY AI Assistant",
        "version": "5.0",
        "platform": "Databricks Apps",
        "legal_sky_available": LEGAL_SKY_AVAILABLE,
        "sarvam_configured": bool(SARVAM_KEY),
        "mode": "LIVE" if (SARVAM_KEY and LEGAL_SKY_AVAILABLE) else "DEMO",
        "features": [
            "Audio input",
            "Text input",
            "Automatic language detection",
            "English passthrough",
            "Regional language to English translation",
            "English to regional language response translation",
            "Intent classification",
            "RAG pipeline"
        ]
    }

@app.post("/api/legal-query", response_model=QueryResponse)
async def legal_query(request: LegalQueryRequest):
    """
    Unified endpoint:
    - accepts audio_data OR query
    - converts input to English
    - runs RAG in English
    - converts answer back to original language
    - works for English directly too
    """
    try:
        if not LEGAL_SKY_AVAILABLE:
            return QueryResponse(
                success=False,
                status="error",
                error="Legal-SKY modules not available",
                message="Backend logic modules are not available"
            )

        regional_input = None
        detected_lang = request.language or "en-IN"

        # -------------------------
        # INPUT HANDLING
        # -------------------------
        if request.audio_data:
            if not SARVAM_KEY:
                return QueryResponse(
                    success=False,
                    status="error",
                    error="SARVAM_API_KEY not configured for audio processing",
                    message="Audio input requires SARVAM_API_KEY"
                )

            logger.info("Step 1: Processing audio input")
            regional_input, detected_lang = auto_detect_and_process(request.audio_data)

        elif request.query and request.query.strip():
            logger.info("Step 1: Processing text input")
            regional_input = request.query.strip()

        else:
            return QueryResponse(
                success=False,
                status="error",
                error="Either audio_data or query must be provided"
            )

        # -------------------------
        # TRANSLATE INPUT TO ENGLISH
        # -------------------------
        logger.info(f"Step 2: Translating input to English from {detected_lang}")
        english_query = translate_to_english(regional_input, detected_lang)

        # -------------------------
        # RUN RAG LOGIC
        # -------------------------
        logger.info("Step 3: Running legal RAG pipeline")
        legal_result = handle_user_query(
            query=english_query,
            original_language=detected_lang
        )

        english_legal_answer = legal_result.get("final_answer", "")

        # -------------------------
        # TRANSLATE ANSWER BACK
        # -------------------------
        logger.info(f"Step 4: Translating answer back to {detected_lang}")
        final_legal_answer = translate_from_english(english_legal_answer, detected_lang)

        return QueryResponse(
            success=True,
            status="complete",
            detected_language=detected_lang,
            regional_input=regional_input,
            english_query=english_query,
            legal_answer=final_legal_answer,
            english_legal_answer=english_legal_answer,
            intents=legal_result.get("intents", []),
            intent_scores=legal_result.get("intent_scores", {}),
            sources=legal_result.get("sources", []),
            action_pack=legal_result.get("action_pack")
        )

    except Exception as e:
        logger.error(f"Legal query error: {str(e)}", exc_info=True)
        return QueryResponse(
            success=False,
            status="error",
            error=str(e),
            message=f"Processing failed: {str(e)}"
        )

# =========================
# STARTUP
# =========================
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 70)
    logger.info("🚀 LEGAL-SKY AI ASSISTANT STARTING")
    logger.info("=" * 70)
    logger.info(f"Legal-SKY: {'✅ Loaded' if LEGAL_SKY_AVAILABLE else '❌ Not Available'}")
    logger.info(f"Sarvam API: {'✅ Configured' if SARVAM_KEY else '❌ Not Set'}")
    logger.info(f"Frontend: {'✅ Available' if frontend_dist.exists() else '❌ Not Built'}")
    logger.info(f"Mode: {'🟢 LIVE' if (SARVAM_KEY and LEGAL_SKY_AVAILABLE) else '🟡 LIMITED'}")
    logger.info("=" * 70)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)