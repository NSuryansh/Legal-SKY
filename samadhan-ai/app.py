import base64
import requests
import logging
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# =========================
# CONFIG
# =========================

SARVAM_KEY = "YOUR_SARVAM_API_KEY"

SARVAM_ASR_ENDPOINT = "https://api.sarvam.ai/speech-to-text"
SARVAM_TRANSLATE_ENDPOINT = "https://api.sarvam.ai/translate"

# =========================
# LOGGER
# =========================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("legal-ai-backend")

# =========================
# FASTAPI INIT
# =========================

app = FastAPI(
    title="Legal AI Assistant API",
    description="Voice + Text Legal Assistant powered by RAG",
    version="1.0"
)

# =========================
# REQUEST MODELS
# =========================

class AudioProcessRequest(BaseModel):
    audio_data: str


class TextQueryRequest(BaseModel):
    query: str
    language: Optional[str] = "en-IN"


# =========================
# RESPONSE MODELS
# =========================

class QueryResponse(BaseModel):
    success: bool
    detected_language: str
    english_query: str
    response: Optional[str] = None
    error: Optional[str] = None


# =========================
# UTIL FUNCTIONS
# =========================

def is_english_language(code: str) -> bool:
    if not code:
        return False
    return code.lower().startswith("en")


# =========================
# ASR + AUTO DETECT
# =========================

def speech_to_text(base64_audio: str):

    try:
        audio_bytes = base64.b64decode(base64_audio)

        files = {
            "file": ("audio.wav", audio_bytes, "audio/wav")
        }

        headers = {
            "api-subscription-key": SARVAM_KEY
        }

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

        return transcript, language

    except Exception as e:
        logger.error(f"ASR Error: {str(e)}")
        raise


# =========================
# TRANSLATE TO ENGLISH
# =========================

def translate_to_english(text: str, source_lang: str):

    try:
        headers = {
            "api-subscription-key": SARVAM_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "input": text,
            "source_language_code": source_lang,
            "target_language_code": "en-IN",
            "mode": "formal"
        }

        response = requests.post(
            SARVAM_TRANSLATE_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        translated_text = result.get("translated_text")

        if not translated_text:
            raise ValueError("Translation returned empty text")

        return translated_text

    except Exception as e:
        logger.error(f"Translation Error: {str(e)}")
        raise


# =========================
# QUERY PROCESSING
# =========================

def process_query(query: str, language: str):

    try:

        # Skip translation if English
        if is_english_language(language):

            english_query = query
            detected_language = "en-IN"

            logger.info("English detected → skipping translation")

        else:

            english_query = translate_to_english(query, language)
            detected_language = language

        logger.info(f"English Query: {english_query}")

        # =========================
        # CALL YOUR RAG SYSTEM
        # =========================

        intents = ["legal_advice"]  # temporary placeholder

        rag_result = run_rag_pipeline(english_query, intents)

        return {
            "success": True,
            "detected_language": detected_language,
            "english_query": english_query,
            "response": rag_result
        }

    except Exception as e:

        logger.error(f"Query Processing Error: {str(e)}")

        return {
            "success": False,
            "detected_language": language,
            "english_query": query,
            "error": str(e)
        }


# =========================
# AUDIO ENDPOINT
# =========================

@app.post("/api/audio-query", response_model=QueryResponse)
def audio_query(request: AudioProcessRequest):

    try:

        transcript, language = speech_to_text(request.audio_data)

        result = process_query(transcript, language)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Audio processing failed: {str(e)}"
        )


# =========================
# TEXT ENDPOINT
# =========================

@app.post("/api/text-query", response_model=QueryResponse)
def text_query(request: TextQueryRequest):

    try:

        result = process_query(
            query=request.query,
            language=request.language
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Text query failed: {str(e)}"
        )


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "legal-ai-backend"
    }