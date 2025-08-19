# 🚀 Neo AI Tutor - Google Cloud Run Deployment Guide

This guide will help you deploy your MATTHSos.py application to Google Cloud Run.

## 📋 Prerequisites

Before deploying, ensure you have the following installed:

### 1. Google Cloud CLI (gcloud)
```bash
# Install gcloud CLI
# Windows: https://cloud.google.com/sdk/docs/install#windows
# macOS: https://cloud.google.com/sdk/docs/install#mac
# Linux: https://cloud.google.com/sdk/docs/install#linux

# Verify installation
gcloud --version
```

### 2. Docker
```bash
# Install Docker Desktop
# https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
```

### 3. Google Cloud Project
- Create a new project or use an existing one
- Note down your Project ID
- Enable billing for the project

## 🔧 Setup Steps

### Step 1: Authenticate with Google Cloud
```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID
```

### Step 2: Enable Required APIs
```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com
```

### Step 3: Configure Environment Variables

Create a `.env` file in your project root with your API keys:

```env
# API Keys (Required)
OPENROUTER_API_KEY=your_openrouter_api_key_here
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here

# Optional API Keys
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Application Configuration
APP_TITLE=Neo - AI Tutor
APP_LAYOUT=wide
SIDEBAR_STATE=expanded

# Database Configuration
DATABASE_NAME=math_tutor.db

# Video Generation Settings
MANIM_QUALITY=ql
VIDEO_FPS=15
VIDEO_RESOLUTION=480p

# Audio Settings
AUDIO_LANGUAGE=en
AUDIO_OUTPUT_FORMAT=mp3

# Security Settings
PASSWORD_HASH_ALGORITHM=sha256
```

## 🚀 Deployment Methods

### Method 1: Automated Deployment (Recommended)

#### Using the Deployment Script

**For Linux/macOS:**
```bash
# Make the script executable
chmod +x deploy.sh

# Update the PROJECT_ID in deploy.sh
# Then run:
./deploy.sh
```

**For Windows (PowerShell):**
```powershell
# Run the PowerShell script
.\deploy.ps1 -ProjectId "your-project-id"
```

### Method 2: Manual Deployment

#### Step 1: Build and Push Docker Image
```bash
# Build the Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/neo-ai-tutor .

# Push to Container Registry
docker push gcr.io/YOUR_PROJECT_ID/neo-ai-tutor
```

#### Step 2: Deploy to Cloud Run
```bash
gcloud run deploy neo-ai-tutor \
  --image gcr.io/YOUR_PROJECT_ID/neo-ai-tutor \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --concurrency 80 \
  --max-instances 10 \
  --set-env-vars "STREAMLIT_SERVER_PORT=8080,STREAMLIT_SERVER_ADDRESS=0.0.0.0,STREAMLIT_SERVER_HEADLESS=true"
```

#### Step 3: Set Environment Variables
```bash
# Set each environment variable from your .env file
gcloud run services update neo-ai-tutor \
  --region us-central1 \
  --update-env-vars "OPENROUTER_API_KEY=your_key_here"

gcloud run services update neo-ai-tutor \
  --region us-central1 \
  --update-env-vars "GOOGLE_GEMINI_API_KEY=your_key_here"

# Continue for all other environment variables...
```

### Method 3: Using Cloud Build (CI/CD)

#### Step 1: Connect to GitHub (Optional)
```bash
# Connect your repository to Cloud Build
gcloud builds submit --config cloudbuild.yaml .
```

#### Step 2: Set up Cloud Build Trigger
1. Go to Cloud Build > Triggers
2. Create a new trigger
3. Connect your repository
4. Use the `cloudbuild.yaml` configuration

## 🔍 Verification

### Check Deployment Status
```bash
# List Cloud Run services
gcloud run services list

# Get service details
gcloud run services describe neo-ai-tutor --region us-central1
```

### Test the Application
```bash
# Get the service URL
gcloud run services describe neo-ai-tutor \
  --region us-central1 \
  --format "value(status.url)"
```

Visit the URL in your browser to test the application.

## ⚙️ Configuration Options

### Resource Allocation
- **Memory**: 2Gi (recommended for video processing)
- **CPU**: 2 cores
- **Timeout**: 3600 seconds (1 hour for video generation)
- **Concurrency**: 80 requests per instance
- **Max Instances**: 10 (adjust based on expected load)

### Environment Variables
All environment variables from your `.env` file will be automatically set during deployment.

## 🔒 Security Considerations

### API Key Management
- ✅ Environment variables are encrypted at rest
- ✅ Keys are not exposed in logs
- ✅ Use different keys for development/production
- ✅ Rotate keys regularly

### Access Control
- The application is set to `--allow-unauthenticated` for public access
- For private access, remove this flag and configure IAM

## 📊 Monitoring and Logging

### View Logs
```bash
# View application logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=neo-ai-tutor" --limit=50
```

### Monitor Performance
1. Go to Cloud Run in Google Cloud Console
2. Select your service
3. View metrics and logs

## 🔄 Updating the Application

### Automatic Updates (with Cloud Build)
Push changes to your connected repository, and Cloud Build will automatically deploy updates.

### Manual Updates
```bash
# Rebuild and redeploy
docker build -t gcr.io/YOUR_PROJECT_ID/neo-ai-tutor .
docker push gcr.io/YOUR_PROJECT_ID/neo-ai-tutor
gcloud run deploy neo-ai-tutor --image gcr.io/YOUR_PROJECT_ID/neo-ai-tutor --region us-central1
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Build Failures
```bash
# Check Docker build locally
docker build -t test-image .

# Check for missing dependencies
docker run --rm test-image python -c "import streamlit; print('OK')"
```

#### 2. Runtime Errors
```bash
# Check application logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=neo-ai-tutor" --limit=100
```

#### 3. Environment Variables Not Set
```bash
# Verify environment variables
gcloud run services describe neo-ai-tutor --region us-central1 --format="value(spec.template.spec.containers[0].env[].name)"
```

#### 4. Memory Issues
- Increase memory allocation: `--memory 4Gi`
- Check for memory leaks in video generation

#### 5. Timeout Issues
- Increase timeout: `--timeout 7200` (2 hours)
- Optimize video generation process

### Performance Optimization

#### 1. Cold Start Optimization
- Use `--min-instances 1` to keep one instance warm
- Optimize Docker image size

#### 2. Resource Optimization
- Monitor CPU and memory usage
- Adjust resource allocation based on usage patterns

#### 3. Cost Optimization
- Set appropriate `--max-instances`
- Use `--cpu-throttling` for cost savings
- Monitor usage in Google Cloud Console

## 📈 Scaling

### Automatic Scaling
Cloud Run automatically scales based on:
- CPU utilization
- Memory usage
- Request volume

### Manual Scaling
```bash
# Set minimum instances
gcloud run services update neo-ai-tutor \
  --region us-central1 \
  --min-instances 1

# Set maximum instances
gcloud run services update neo-ai-tutor \
  --region us-central1 \
  --max-instances 20
```

## 🗑️ Cleanup

### Remove the Service
```bash
# Delete the Cloud Run service
gcloud run services delete neo-ai-tutor --region us-central1

# Remove Docker images
gcloud container images delete gcr.io/YOUR_PROJECT_ID/neo-ai-tutor --force-delete-tags
```

## 📞 Support

If you encounter issues:

1. **Check the logs**: Use `gcloud logs read` command
2. **Verify configuration**: Ensure all environment variables are set
3. **Test locally**: Run the application locally first
4. **Check quotas**: Ensure you haven't exceeded Google Cloud quotas

## 🎉 Success!

Once deployed, your Neo AI Tutor application will be available at the provided URL. The application will automatically scale based on demand and provide a robust, production-ready environment for your AI-powered mathematics tutoring platform. 