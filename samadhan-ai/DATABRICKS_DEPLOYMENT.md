# 🚀 Deploy Samadhan AI on Databricks Platform

This guide shows you how to deploy the **entire application on Databricks** and access it directly from your workspace!

## 🎯 What You'll Get

* ✅ **Full-Stack App on Databricks** - No need for external servers
* ✅ **Automatic Scaling** - Serverless compute handles traffic
* ✅ **Secure** - API keys managed as environment variables
* ✅ **Easy Access** - Direct link in your Databricks workspace
* ✅ **Real Sarvam AI** - Connected to 01_Sarvam_Gateway notebook

---

## 📋 Prerequisites

1. **Databricks Workspace** (AWS, Azure, or GCP)
2. **Databricks CLI** installed locally
3. **Node.js & npm** for building the frontend

---

## 🏗️ Architecture

```
┌──────────────────────────────────────┐
│   Databricks Workspace              │
│                                      │
│  ┌────────────────────────────────┐ │
│  │   Samadhan AI App              │ │
│  │   (Serverless Compute)         │ │
│  │                                │ │
│  │  ┌──────────────────────────┐ │ │
│  │  │  FastAPI Backend         │ │ │
│  │  │  - /api/process-audio    │ │ │
│  │  │  - /api/health           │ │ │
│  │  │  - Sarvam AI Integration │ │ │
│  │  └──────────────────────────┘ │ │
│  │                                │ │
│  │  ┌──────────────────────────┐ │ │
│  │  │  React Frontend          │ │ │
│  │  │  - Beautiful UI          │ │ │
│  │  │  - Voice Recording       │ │ │
│  │  │  - Results Display       │ │ │
│  │  └──────────────────────────┘ │ │
│  └────────────────────────────────┘ │
│                                      │
│  Environment: SARVAM_API_KEY         │
└──────────────────────────────────────┘
           ↓
    ┌─────────────┐
    │  Sarvam AI  │
    │   APIs      │
    └─────────────┘
```

---

## 🚀 Deployment Steps

### Step 1: Build the Frontend

```bash
cd samadhan-ai/frontend

# Install dependencies
npm install

# Build for production
npm run build

# This creates frontend/dist/ folder with optimized files
```

### Step 2: Prepare the Application

The following files are already configured:
* ✅ `app.yaml` - Databricks App configuration
* ✅ `app.py` - Unified backend + frontend server
* ✅ `backend/.env` - Sarvam API key

### Step 3: Install Databricks CLI

```bash
# If not already installed
pip install databricks-cli

# Configure authentication
databricks configure --token
```

You'll be asked for:
* **Databricks Host**: Your workspace URL (e.g., `https://your-workspace.cloud.databricks.com`)
* **Token**: Generate from User Settings → Access Tokens

### Step 4: Create the Databricks App

#### Option A: Using Databricks CLI

```bash
cd samadhan-ai

# Create the app
databricks apps create samadhan-ai

# This will:
# 1. Upload all files to Databricks
# 2. Create serverless compute
# 3. Deploy the application
# 4. Return the app URL
```

#### Option B: Using Databricks UI

1. Go to your Databricks workspace
2. Click **"Apps"** in the left sidebar
3. Click **"Create App"**
4. Choose **"From Code"**
5. Upload the `samadhan-ai` folder
6. Click **"Deploy"**

### Step 5: Access Your App

After deployment, you'll get a URL like:
```
https://<workspace-url>/apps/samadhan-ai
```

Click it to open your deployed application! 🎉

---

## 🔧 Configuration

### Environment Variables (app.yaml)

```yaml
env:
  - name: SARVAM_API_KEY
    value: sk_sn9w8roe_QwQ3Sc7Xa9acvNvTh5iV8Iek
```

**Security Note**: For production, use Databricks Secrets instead:

```yaml
env:
  - name: SARVAM_API_KEY
    valueFrom:
      secretKeyRef:
        scope: api-keys
        key: sarvam-api-key
```

### Resource Configuration

```yaml
resources:
  memory: "2Gi"    # Increase if needed
  cpu: "1"         # Increase for high traffic
```

---

## 📊 Monitoring & Management

### View App Status

```bash
# List all apps
databricks apps list

# Get app details
databricks apps get samadhan-ai

# View logs
databricks apps logs samadhan-ai
```

### Update the App

```bash
# After making changes
cd samadhan-ai
databricks apps deploy samadhan-ai
```

### Delete the App

```bash
databricks apps delete samadhan-ai
```

---

## 🧪 Testing the Deployed App

### Health Check

```bash
curl https://<your-workspace>/apps/samadhan-ai/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Samadhan AI - Databricks App",
  "version": "2.0.0",
  "platform": "Databricks Apps",
  "sarvam_configured": true,
  "mode": "LIVE"
}
```

### Test Audio Processing

1. Open the app URL in your browser
2. Click the microphone button
3. Speak in Hindi (or any regional language)
4. Watch the real-time transcription and translation!

---

## 🐛 Troubleshooting

### App not starting

**Check logs:**
```bash
databricks apps logs samadhan-ai
```

**Common issues:**
* Missing `frontend/dist/` folder → Run `npm run build` first
* API key not set → Check `app.yaml` env variables
* Port conflict → Databricks Apps use port 8080 by default

### Frontend not loading

* Verify `frontend/dist/` exists and has `index.html`
* Check that `app.py` mounts static files correctly
* Clear browser cache

### API not responding

* Check Sarvam API key is valid
* Verify `SARVAM_API_KEY` environment variable is set
* Check network connectivity from Databricks

### Microphone not working

* Must use HTTPS (Databricks Apps are always HTTPS ✅)
* Grant browser microphone permissions
* Use Chrome or Edge for best compatibility

---

## 🔒 Security Best Practices

### 1. Use Databricks Secrets

```bash
# Create secret scope
databricks secrets create-scope --scope api-keys

# Add Sarvam API key
databricks secrets put --scope api-keys --key sarvam-api-key
```

Update `app.yaml`:
```yaml
env:
  - name: SARVAM_API_KEY
    valueFrom:
      secretKeyRef:
        scope: api-keys
        key: sarvam-api-key
```

### 2. Enable Authentication

Add to `app.yaml`:
```yaml
authentication:
  enabled: true
  requireLogin: true
```

### 3. Set CORS Restrictions

In `app.py`, replace `allow_origins=["*"]` with:
```python
allow_origins=[
    "https://your-workspace.cloud.databricks.com"
]
```

---

## 📈 Scaling & Performance

### Auto-Scaling

Databricks Apps automatically scale based on traffic. No configuration needed! ✅

### Increase Resources

Edit `app.yaml`:
```yaml
resources:
  memory: "4Gi"    # For high traffic
  cpu: "2"         # More processing power
```

### Monitor Performance

```bash
# View app metrics
databricks apps metrics samadhan-ai

# View resource usage
databricks apps stats samadhan-ai
```

---

## 🎯 Production Checklist

Before going live:

- [ ] Built frontend (`npm run build`)
- [ ] Tested locally (`python app.py`)
- [ ] API key configured as secret (not hardcoded)
- [ ] CORS restricted to your domain
- [ ] Authentication enabled
- [ ] Resource limits set appropriately
- [ ] Logs monitored
- [ ] Backup plan for Sarvam AI quota limits

---

## 🆚 Deployment Comparison

 Feature | Local Deployment | Databricks Apps |
---------|-----------------|----------------|
 **Setup Time** | 10-15 minutes | 5 minutes |
 **Maintenance** | Manual updates | Auto-scaling |
 **Security** | Self-managed | Built-in |
 **Access** | localhost only | Workspace users |
 **Scaling** | Manual | Automatic |
 **Cost** | Server costs | Pay-per-use |

---

## 📚 Additional Resources

* [Databricks Apps Documentation](https://docs.databricks.com/apps)
* [Databricks CLI Guide](https://docs.databricks.com/dev-tools/cli)
* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [React Deployment](https://vitejs.dev/guide/build.html)

---

## 🎉 Success!

Your Samadhan AI application is now:
* ✅ Deployed on Databricks
* ✅ Accessible from your workspace
* ✅ Using real Sarvam AI translation
* ✅ Auto-scaling with traffic
* ✅ Production-ready!

---

**Need help?** Check the logs or contact your Databricks administrator.

**Want to demo?** Share the app URL with your team/judges!
