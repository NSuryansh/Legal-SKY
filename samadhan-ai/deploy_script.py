#!/usr/bin/env python
"""
Samadhan AI - Deployment Package Creator
Run this script to create a ZIP file for deployment
"""

import zipfile
import os

# Configuration
APP_NAME = "samadhan-ai"
SOURCE_PATH = "/dbfs/Workspace/Shared/samadhan-ai"
OUTPUT_ZIP = "/dbfs/tmp/samadhan-ai-deploy.zip"

print("=" * 70)
print("🚀 Samadhan AI Deployment Package Creator")
print("=" * 70)
print(f"\n📁 Source: {SOURCE_PATH}")
print(f"💾 Output: {OUTPUT_ZIP}")
print("-" * 70)

def create_zip():
    print("\n📦 Creating deployment ZIP...\n")
    
    try:
        os.makedirs(os.path.dirname(OUTPUT_ZIP), exist_ok=True)
        
        files_to_include = [
            ("app.yaml", "App configuration"),
            ("app.py", "Backend server"),
            ("requirements.txt", "Python dependencies"),
            ("frontend/dist/index.html", "Frontend HTML")
        ]
        
        with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
            files_added = 0
            
            for rel_path, description in files_to_include:
                full_path = os.path.join(SOURCE_PATH, rel_path)
                
                if os.path.exists(full_path):
                    zipf.write(full_path, rel_path)
                    size = os.path.getsize(full_path)
                    print(f"   ✅ {rel_path:35s} ({size:,} bytes)")
                    files_added += 1
                else:
                    print(f"   ⚠️  {rel_path:35s} - NOT FOUND")
        
        if files_added > 0:
            zip_size = os.path.getsize(OUTPUT_ZIP)
            print(f"\n✅ ZIP created successfully!")
            print(f"   Files: {files_added}")
            print(f"   Size: {zip_size:,} bytes ({zip_size/1024:.2f} KB)")
            print(f"   Location: {OUTPUT_ZIP}")
            print(f"   DBFS path: dbfs:/tmp/samadhan-ai-deploy.zip")
            return True
        else:
            print("\n❌ No files added!")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_zip()
    
    if success:
        print("\n" + "=" * 70)
        print("📖 DEPLOYMENT INSTRUCTIONS")
        print("=" * 70)
        print("\n🖥️  UI Deployment (Recommended):")
        print("-" * 70)
        print("1. Go to: Compute → Apps → samadhan-ai → Edit")
        print("2. In Step 2 (Git), look for 'Upload files' option")
        print("3. Upload: /tmp/samadhan-ai-deploy.zip")
        print("   (Download from DBFS browser first)")
        print("4. Click Next → Deploy")
        print("5. Wait 2-5 minutes")
        print("6. Access your app URL!")
        print("\n📁 Or use workspace path:")
        print("   Source: /Shared/samadhan-ai")
        print("   Config: app.yaml")
        print("=" * 70)
