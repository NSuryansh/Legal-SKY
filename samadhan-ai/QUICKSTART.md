# 🚀 QUICKSTART - Run Samadhan AI in 5 Minutes

## ✅ Prerequisites (One-time setup)
- Node.js 18+ installed
- Python 3.9+ installed

## 📥 Step 1: Download the Project
Download `/Shared/samadhan-ai/` from Databricks to your local machine.

## 🔧 Step 2: Setup (First time only)

### Backend Setup:
```bash
cd samadhan-ai/backend

# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup:
```bash
cd samadhan-ai/frontend

# Install dependencies
npm install
```

## ▶️ Step 3: Run the Application

### Terminal 1 - Start Backend:
```bash
cd samadhan-ai/backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
======================================================================
🚀 SAMADHAN AI BACKEND - CONNECTED TO 01_SARVAM_GATEWAY
======================================================================
📡 Sarvam API Key: ✅ Loaded
🔧 Mode: LIVE (Real Translation)
======================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Start Frontend:
```bash
cd samadhan-ai/frontend
npm run dev
```

You should see:
```
VITE v5.0.8  ready in 500 ms

➜  Local:   http://localhost:5173/
```

## 🎨 Step 4: Open the Application

Open your browser and go to:
```
http://localhost:5173
```

## 🎙️ Step 5: Test Voice Translation

1. **Select Language**: Choose "Hindi (हिंदी)" or any Indian language
2. **Click Microphone**: Click the big blue microphone button
3. **Speak Clearly**: Say something like "मेरा नाम रमेश है"
4. **Click Again to Stop**: Click microphone again
5. **See Magic**: Watch REAL transcription and translation appear!

## 🧪 (Optional) Run Integration Test

Before demoing to others, verify everything works:
```bash
cd samadhan-ai
python test_integration.py
```

Should show:
```
✅ ALL TESTS PASSED!
🎯 Your backend is perfectly connected to 01_Sarvam_Gateway
```

## 📊 What You'll See

### Backend Console:
```
🎙️ Processing incoming audio (hi-IN)...
✅ Transcribed: मेरा नाम रमेश है
✅ Translated for AI: My name is Ramesh
```

### Frontend UI:
Beautiful dashboard showing:
- **Regional Input**: मेरा नाम रमेश है
- **English Translation**: My name is Ramesh

## 🐛 Common Issues

### Issue: Backend won't start
```bash
# Make sure you activated virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
```bash
# Kill existing process
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Frontend won't start
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Microphone not working
- Grant browser microphone permissions
- Use Chrome or Edge (best support)
- Check browser console (F12) for errors

## 🎯 Features Working

✅ Voice Recording (9 Indian languages)
✅ Speech-to-Text (Sarvam AI)
✅ Translation to English (Sarvam AI)
✅ Beautiful React UI
✅ Real-time processing
✅ Query history
✅ Multi-language support

## 📁 Project Structure

```
samadhan-ai/
├── backend/
│   ├── .env              ← Your Sarvam API key
│   ├── main.py           ← Connected to 01_Sarvam_Gateway
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   └── package.json
├── test_integration.py   ← Run this to verify
├── INTEGRATION_GUIDE.md  ← Complete details
└── QUICKSTART.md         ← This file
```

## 🏆 Hackathon Demo Tips

1. **Pre-test Everything**: Run `test_integration.py` before demo
2. **Prepare Phrases**: Have test sentences ready in multiple languages
3. **Show Multiple Languages**: Demo Hindi, Tamil, Bengali to impress
4. **Explain the Flow**: Voice → Sarvam AI → English → RAG (future)
5. **Highlight Tech Stack**: React + FastAPI + Sarvam AI + Databricks

## 🎬 Demo Script

"Hi everyone! This is **Samadhan AI** - a sovereign AI portal for Indian citizens to access legal services in their own language.

Watch this: [Click microphone, speak in Hindi]

See? It transcribed my Hindi perfectly, and translated to English. This English text will feed into our RAG pipeline with legal documents.

The best part? It works in 9 Indian languages! [Show language selector]

Backend is powered by Sarvam AI and runs on Databricks. Frontend is React with Tailwind. All open source, all Made in India!"

## 📞 Need Help?

Check these files:
- `INTEGRATION_GUIDE.md` - Complete technical details
- `README.md` - Full documentation
- Notebook: `/Shared/Legal-SKY/Translation/01_Sarvam_Gateway`

## 🎉 You're Ready!

Your application is:
- ✅ Production-ready
- ✅ Real AI translation working
- ✅ Beautiful UI
- ✅ Ready to demo

**Go win that hackathon! 🏆**
