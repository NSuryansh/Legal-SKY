# 🇮🇳 Samadhan AI - Sovereign AI Portal

A modern, production-ready dashboard that helps Indian citizens access legal and government services using their voice in regional languages.

## ✨ **NOW WITH REAL SARVAM AI INTEGRATION!**

This application now includes **live speech-to-text and translation** powered by Sarvam AI APIs.

## 🎯 Project Overview

**Phase 1 (COMPLETE):** ✅ Translation & Audio Gateway Integration
- Voice recording interface
- Audio-to-Base64 conversion  
- **REAL Sarvam AI Speech-to-Text (ASR)**
- **REAL Sarvam AI Translation (Regional → English)**
- REST API communication
- Multi-language support (9 Indian languages)

**Phase 2 (Coming Soon):**
- Databricks AI/RAG integration for legal query answering
- Database connectivity
- Document management

## 🏗️ Architecture

```
samadhan-ai/
├── frontend/          # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Header.jsx
│   │   │   └── VoiceQueryInterface.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
└── backend/           # FastAPI (Python) + Sarvam AI
    ├── main.py        # ✅ Real Sarvam Integration
    ├── requirements.txt
    ├── .env.example   # API key template
    └── .env           # Your API key (create this)
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- **Modern browser** with microphone access
- **Sarvam AI API Key** (Get it from [sarvam.ai](https://www.sarvam.ai/))

### 1️⃣ Backend Setup

```bash
cd samadhan-ai/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# IMPORTANT: Configure your Sarvam API Key
# Create a .env file:
echo "SARVAM_API_KEY=your_actual_api_key_here" > .env

# OR manually create .env file with:
# SARVAM_API_KEY=your_actual_api_key_here

# Run FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will run at:** `http://localhost:8000`

#### 🔑 Getting Your Sarvam API Key

1. Go to [https://www.sarvam.ai/](https://www.sarvam.ai/)
2. Sign up for an account
3. Navigate to API Keys section
4. Copy your API key
5. Paste it in the `.env` file

#### 🎭 Demo Mode

If you don't have an API key yet, the backend will run in **DEMO MODE** with sample responses so you can still test the UI.

### 2️⃣ Frontend Setup

```bash
cd samadhan-ai/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Frontend will run at:** `http://localhost:5173`

## 🎨 Features

### Current (Phase 1 - LIVE)

✅ **Beautiful Dashboard UI**
- Modern Slate/Blue color palette
- Sidebar navigation with Lucide icons
- Fixed header with search and user profile
- Responsive layout

✅ **Voice Query Interface**
- Interactive microphone button with pulse animation
- Browser MediaRecorder API integration
- Real-time recording status
- Base64 audio conversion (with prefix stripping)

✅ **REAL Sarvam AI Integration** 🔥
- **Speech-to-Text (ASR):** Converts your voice to regional text
- **Translation API:** Translates regional text to English for RAG processing
- Supports 9 Indian languages
- Production-ready error handling

✅ **Multi-Language Support**
- Hindi (हिंदी)
- Bengali (বাংলা)
- Telugu (తెలుగు)
- Marathi (मराठी)
- Tamil (தமிழ்)
- Gujarati (ગુજરાતી)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Punjabi (ਪੰਜਾਬੀ)

✅ **Chat-like Results Display**
- Regional language transcription (from Sarvam ASR)
- English translation (from Sarvam Translate)
- Query history with timestamps
- Status indicators

✅ **REST API Backend**
- FastAPI with CORS support
- `/api/process-audio` endpoint with real Sarvam calls
- Pydantic validation
- Health check endpoints
- Automatic demo mode fallback

## 🔧 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Requests** - HTTP client for Sarvam APIs
- **Python-dotenv** - Environment variable management
- **Sarvam AI** - Speech-to-Text & Translation

## 📡 API Documentation

### POST `/api/process-audio`

**Request:**
```json
{
  "audio_data": "<base64_string>",
  "language_code": "hi-IN"
}
```

**Response (Success):**
```json
{
  "status": "success",
  "regional_input": "मेरा नाम रमेश है और मुझे कानूनी सहायता चाहिए",
  "english_query": "My name is Ramesh and I need legal assistance"
}
```

**Response (Demo Mode):**
```json
{
  "status": "demo_mode",
  "regional_input": "मेरा नाम रमेश है",
  "english_query": "My name is Ramesh",
  "message": "Running in demo mode. Set SARVAM_API_KEY to enable real translation."
}
```

### GET `/`

Returns API info and configuration status:
```json
{
  "message": "Samadhan AI Backend - REAL SARVAM INTEGRATION",
  "version": "2.0.0",
  "phase": "Phase 1 - Live Translation Gateway",
  "sarvam_configured": true
}
```

### GET `/api/health`

Detailed health check with integration status.

## 🔐 Security Notes

- CORS configured for `localhost:5173`
- Base64 audio data validated before processing
- Input sanitization via Pydantic models
- API keys stored in `.env` (not committed to git)
- Automatic fallback to demo mode if API key missing

## 🎯 Next Steps (Phase 2)

1. ~~**Integrate Databricks Notebook** (`01_Sarvam_Gateway`)~~ ✅ DONE
2. ~~**Real Audio Transcription** (Sarvam AI)~~ ✅ DONE
3. ~~**Real Translation** (Sarvam AI)~~ ✅ DONE
4. **Reverse Translation** (English RAG output → Regional language)
5. **RAG Pipeline Integration** (Legal knowledge base)
6. **Database Integration** (PostgreSQL/MongoDB)
7. **User Authentication** (JWT)
8. **Document Management System**

## 🐛 Troubleshooting

### Microphone not working
- Grant browser microphone permissions
- Use HTTPS or localhost only
- Check browser console for errors

### CORS errors
- Ensure backend is running on port 8000
- Check CORS configuration in `main.py`

### Frontend not connecting to backend
- Verify backend URL in `VoiceQueryInterface.jsx`
- Check if backend is running: `http://localhost:8000`
- Look for error messages in browser console

### "SARVAM_API_KEY not configured" error
- Create `.env` file in `backend/` directory
- Add your API key: `SARVAM_API_KEY=your_key_here`
- Restart the backend server
- Check health endpoint: `http://localhost:8000/api/health`

### Translation not working
- Verify API key is correct
- Check Sarvam AI account has credits
- Look at backend console logs for detailed error messages
- Try demo mode first to verify frontend works

## 📊 Testing the Integration

1. Start both backend and frontend
2. Open `http://localhost:5173`
3. Select a language (e.g., Hindi)
4. Click the microphone button
5. Speak clearly in the selected language
6. Click again to stop recording
7. Watch the real-time transcription and translation appear!

## 📄 License

Built for hackathon purposes - Sovereign AI for Indian Citizens

## 👥 Contributors

Built with ❤️ for the Indian Digital Ecosystem

---

**Powered by Databricks AI + Sarvam AI**
