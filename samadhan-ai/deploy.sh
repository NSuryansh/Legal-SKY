#!/bin/bash

# Samadhan AI - Databricks Deployment Script
# This script automates the deployment process

echo "=================================================================="
echo "🚀 SAMADHAN AI - DATABRICKS DEPLOYMENT"
echo "=================================================================="
echo ""

# Step 1: Build Frontend
echo "📦 Step 1/4: Building React Frontend..."
cd frontend
npm install
npm run build

if [ ! -d "dist" ]; then
    echo "❌ Frontend build failed! dist/ folder not found."
    exit 1
fi

echo "✅ Frontend built successfully!"
cd ..

# Step 2: Verify Files
echo ""
echo "🔍 Step 2/4: Verifying deployment files..."

required_files=("app.yaml" "app.py" "backend/.env")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

echo "✅ All required files present!"

# Step 3: Test Locally (Optional)
echo ""
echo "🧪 Step 3/4: Would you like to test locally first? (y/n)"
read -r test_local

if [ "$test_local" = "y" ]; then
    echo "Starting local server on port 8080..."
    python app.py &
    SERVER_PID=$!
    
    echo "Waiting for server to start..."
    sleep 3
    
    # Test health endpoint
    if curl -s http://localhost:8080/api/health | grep -q "healthy"; then
        echo "✅ Local server is healthy!"
        kill $SERVER_PID
    else
        echo "❌ Local server health check failed!"
        kill $SERVER_PID
        exit 1
    fi
fi

# Step 4: Deploy to Databricks
echo ""
echo "🚀 Step 4/4: Deploying to Databricks..."
echo ""
echo "Choose deployment method:"
echo "  1) Databricks CLI (automated)"
echo "  2) Manual upload (I'll do it myself)"
read -r deploy_method

if [ "$deploy_method" = "1" ]; then
    echo ""
    echo "📤 Deploying with Databricks CLI..."
    
    # Check if databricks CLI is installed
    if ! command -v databricks &> /dev/null; then
        echo "❌ Databricks CLI not found!"
        echo "Install it with: pip install databricks-cli"
        exit 1
    fi
    
    # Deploy the app
    databricks apps create samadhan-ai
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=================================================================="
        echo "✅ DEPLOYMENT SUCCESSFUL!"
        echo "=================================================================="
        echo ""
        echo "Your app is now live on Databricks!"
        echo ""
        echo "Next steps:"
        echo "  1. Go to your Databricks workspace"
        echo "  2. Navigate to 'Apps' in the left sidebar"
        echo "  3. Click 'samadhan-ai' to open your app"
        echo ""
        echo "Or use: databricks apps get samadhan-ai"
        echo "=================================================================="
    else
        echo "❌ Deployment failed! Check the error message above."
        exit 1
    fi
else
    echo ""
    echo "📋 Manual Deployment Instructions:"
    echo "=================================================================="
    echo "1. Go to your Databricks workspace"
    echo "2. Click 'Apps' → 'Create App'"
    echo "3. Choose 'From Code'"
    echo "4. Upload the entire samadhan-ai folder"
    echo "5. Click 'Deploy'"
    echo "=================================================================="
fi

echo ""
echo "🎉 Done! Your hackathon project is ready to impress!"
