# 🚀 Quick Deployment Guide for Neo AI Tutor

## Current Issue
The gcloud CLI is not installed or not in your PATH. Let's fix this step by step.

## 🔧 Step 1: Install Google Cloud CLI

### Option A: Automatic Installation (Recommended)
```powershell
# Run the setup script
.\setup-gcloud.ps1
```

### Option B: Manual Installation
1. **Download the installer:**
   - Go to: https://cloud.google.com/sdk/docs/install#windows
   - Download "Google Cloud SDK Installer for Windows"

2. **Run the installer:**
   - Run as Administrator
   - Follow the installation wizard
   - **Important:** Restart your terminal after installation

3. **Verify installation:**
   ```powershell
   gcloud --version
   ```

## 🔐 Step 2: Authenticate with Google Cloud

```powershell
# Login to Google Cloud
gcloud auth login
```

This will open a browser window for authentication.

## 📋 Step 3: Set Your Project

```powershell
# List available projects
gcloud projects list

# Set your project (replace with your actual project ID)
gcloud config set project talk-2-doc
```

## 🐳 Step 4: Verify Docker Installation

```powershell
# Check if Docker is installed
docker --version

# Check if Docker daemon is running
docker info
```

If Docker is not running, start Docker Desktop.

## 🚀 Step 5: Deploy Your Application

### Test your setup first:
```powershell
.\test-gcloud.ps1
```

### If everything is working, deploy:
```powershell
.\deploy-windows.ps1
```

## 📁 Files Created for Deployment

1. **`Dockerfile`** - Container configuration
2. **`.dockerignore`** - Files to exclude from container
3. **`cloudbuild.yaml`** - Cloud Build configuration
4. **`deploy.sh`** - Linux/macOS deployment script
5. **`deploy-windows.ps1`** - Windows PowerShell deployment script
6. **`setup-gcloud.ps1`** - Google Cloud CLI setup script
7. **`test-gcloud.ps1`** - Environment verification script
8. **`app.yaml`** - App Engine configuration (alternative)
9. **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment guide

## 🔑 Environment Variables

Make sure your `.env` file contains:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here
```

## 🛠️ Troubleshooting

### If gcloud is not found after installation:
1. **Restart your terminal/PowerShell**
2. **Check PATH environment variable:**
   ```powershell
   $env:PATH -split ';' | Where-Object { $_ -like '*Google*' }
   ```
3. **Add to PATH manually if needed:**
   ```powershell
   $env:PATH += ";C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin"
   ```

### If Docker is not found:
1. **Install Docker Desktop:** https://www.docker.com/products/docker-desktop
2. **Start Docker Desktop**
3. **Restart your terminal**

### If authentication fails:
```powershell
# Clear existing credentials
gcloud auth revoke --all

# Login again
gcloud auth login
```

### If project access is denied:
1. **Check if you have access to the project**
2. **Verify billing is enabled**
3. **Check IAM permissions**

## 📞 Quick Commands

```powershell
# Test everything
.\test-gcloud.ps1

# Setup gcloud
.\setup-gcloud.ps1

# Deploy application
.\deploy-windows.ps1

# Check deployment status
gcloud run services list

# View logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=neo-ai-tutor"
```

## 🎯 Expected Outcome

After successful deployment, you'll get a URL like:
```
https://neo-ai-tutor-xxxxx-uc.a.run.app
```

Your Neo AI Tutor application will be accessible at this URL.

## ⚡ Quick Start (Once gcloud is installed)

```powershell
# 1. Setup and authenticate
.\setup-gcloud.ps1

# 2. Test environment
.\test-gcloud.ps1

# 3. Deploy
.\deploy-windows.ps1
```

That's it! Your application will be live on Google Cloud Run. 🎉 