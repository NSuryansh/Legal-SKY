# ⚡ Samadhan AI - Databricks Quick Deploy (5 Minutes!)

Deploy your entire hackathon project on Databricks in **5 simple steps**!

---

## 🎯 Prerequisites

* ✅ Databricks workspace access
* ✅ Node.js installed on your local machine
* ✅ Terminal/Command prompt

---

## 🚀 5-Step Deployment

### Step 1: Download the Project

If you're working from Databricks notebook:

```bash
# Export the project folder to your local machine
# Navigate to /Shared/samadhan-ai in Databricks workspace
# Click the folder → Export → Download ZIP
```

Or clone if you have it in git:

```bash
git clone <your-repo>
cd samadhan-ai
```

### Step 2: Build Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

**Expected result:** `frontend/dist/` folder created with `index.html`

### Step 3: Quick Test (Optional but Recommended)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Open browser: http://localhost:8080
# Try recording voice → Should see transcription!
```

Press `Ctrl+C` to stop when done testing.

### Step 4: Deploy to Databricks

#### Option A: Using Databricks UI (Easiest! 🎉)

1. **Open Databricks Workspace** → Go to your workspace URL
2. **Click "Apps"** in left sidebar
3. **Click "Create App"**
4. **Choose "From Code"**
5. **Upload** the entire `samadhan-ai` folder
6. **Click "Deploy"** (takes 2-3 minutes)
7. **Done!** Click the app URL to open 🎊

#### Option B: Using Databricks CLI

```bash
# Install CLI
pip install databricks-cli

# Configure (one-time setup)
databricks configure --token
# Enter your workspace URL and token

# Deploy!
cd samadhan-ai
databricks apps create samadhan-ai
```

### Step 5: Access Your App

After deployment completes, you'll see a URL like:

```
https://<your-workspace>.cloud.databricks.com/apps/samadhan-ai
```

**Click it** and your app is live! 🚀

---

## 🎤 Testing Your Deployed App

1. **Click the microphone icon** 🎙️
2. **Allow microphone access** when browser prompts
3. **Speak in Hindi** (or any regional language):
   * "Mujhe divorce ke baare mein jaankari chahiye"
   * "क्या मैं अपनी property sell कर सकता हूं?"
4. **See real-time transcription** in both Hindi and English!

---

## 🔍 Verify Everything Works

### Check Health Status

Visit: `https://<your-workspace>/apps/samadhan-ai/api/health`

**Should see:**
```json
{
  "status": "healthy",
  "service": "Samadhan AI - Databricks App",
  "platform": "Databricks Apps",
  "sarvam_configured": true,
  "mode": "LIVE"
}
```

### Check Sarvam AI Integration

1. Open the app
2. Record voice in Hindi
3. You should see:
   * **Regional Input:** Your Hindi speech transcribed
   * **English Translation:** Translated query

If you see "Demo mode" warnings → Check `SARVAM_API_KEY` in `app.yaml`

---

## 🐛 Troubleshooting

### Frontend doesn't load

```bash
# Check if dist folder exists
ls frontend/dist/

# If missing, rebuild:
cd frontend
npm run build
```

### API not responding

```bash
# Check Databricks App logs
databricks apps logs samadhan-ai

# Common issue: API key not set
# Fix: Edit app.yaml and redeploy
```

### Microphone not working

* ✅ Grant browser permissions
* ✅ Use Chrome or Edge (best compatibility)
* ✅ Ensure HTTPS (Databricks Apps are always HTTPS ✅)

---

## 🎯 What's Next?

Your app is now:
* ✅ **Deployed on Databricks** (no external servers needed!)
* ✅ **Voice-enabled** with 9 Indian languages
* ✅ **AI-powered** with Sarvam AI translation
* ✅ **Production-ready** with auto-scaling
* ✅ **Demo-ready** for your hackathon judges!

### For Your Hackathon Presentation:

1. **Share the app URL** with judges
2. **Demo live voice recording** in Hindi/regional language
3. **Show real-time translation** to English
4. **Explain**: "Runs entirely on Databricks with Sarvam AI"

---

## 📊 App URLs You'll Need

 Purpose | URL |
---------|-----|
 **Main App** | `https://<workspace>/apps/samadhan-ai` |
 **Health Check** | `https://<workspace>/apps/samadhan-ai/api/health` |
 **API Endpoint** | `https://<workspace>/apps/samadhan-ai/api/process-audio` |

---

## 🆘 Need Help?

### Check App Status
```bash
databricks apps get samadhan-ai
```

### View Logs
```bash
databricks apps logs samadhan-ai
```

### Redeploy After Changes
```bash
databricks apps deploy samadhan-ai
```

### Delete App
```bash
databricks apps delete samadhan-ai
```

---

## 🎉 Success Checklist

- [ ] Frontend built (`frontend/dist/` exists)
- [ ] App deployed to Databricks
- [ ] App URL accessible
- [ ] Health check returns "healthy"
- [ ] Voice recording works
- [ ] Sarvam AI translation works
- [ ] Ready to demo! 🏆

---

**🚀 You're all set! Good luck with your hackathon! 🏆**

For detailed documentation, see: [DATABRICKS_DEPLOYMENT.md](./DATABRICKS_DEPLOYMENT.md)
