#!/bin/bash

# Neo AI Tutor - Google Cloud Run Deployment Script
# This script deploys the MATTHSos.py application to Google Cloud Run

set -e  # Exit on any error

# Configuration
PROJECT_ID="arunaiprojects-ai-tutor-469508"  # Replace with your actual project ID
REGION="us-central1"
SERVICE_NAME="neo-ai-tutor"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists gcloud; then
        print_error "Google Cloud SDK (gcloud) is not installed. Please install it first."
        print_status "Visit: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install it first."
        print_status "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Authenticate with Google Cloud
authenticate() {
    print_status "Authenticating with Google Cloud..."
    
    # Check if already authenticated
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        current_account=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n 1)
        print_status "Already authenticated as: $current_account"
    else
        print_warning "No active Google Cloud account found. Please authenticate."
        gcloud auth login
    fi
    
    # Configure Docker to use gcloud as a credential helper
    print_status "Configuring Docker authentication..."
    gcloud auth configure-docker --quiet
    
    print_success "Authentication successful"
}

# Set the project
set_project() {
    print_status "Setting Google Cloud project to: $PROJECT_ID"
    
    # # Check if project exists and is accessible
    # if ! gcloud projects describe "$PROJECT_ID" &> /dev/null; then
    #     print_error "Project $PROJECT_ID not found or you don't have access to it."
    #     print_status "Available projects:"
    #     gcloud projects list --format="table(projectId,name)" | head -10
    #     exit 1
    # fi
    
    # Set the project
    gcloud config set project "$PROJECT_ID"
    
    # Verify project is set
    current_project=$(gcloud config get-value project)
    if [ "$current_project" != "$PROJECT_ID" ]; then
        print_error "Failed to set project to $PROJECT_ID"
        exit 1
    fi
    
    print_success "Project set successfully to: $PROJECT_ID"
}

# Enable required APIs
enable_apis() {
    print_status "Enabling required Google Cloud APIs..."
    
    # Enable APIs with error handling
    print_status "Enabling cloudbuild.googleapis.com..."
    if gcloud services enable cloudbuild.googleapis.com --quiet; then
        print_success "Enabled cloudbuild.googleapis.com"
    else
        print_warning "Failed to enable cloudbuild.googleapis.com (might already be enabled)"
    fi
    
    print_status "Enabling run.googleapis.com..."
    if gcloud services enable run.googleapis.com --quiet; then
        print_success "Enabled run.googleapis.com"
    else
        print_warning "Failed to enable run.googleapis.com (might already be enabled)"
    fi
    
    print_status "Enabling containerregistry.googleapis.com..."
    if gcloud services enable containerregistry.googleapis.com --quiet; then
        print_success "Enabled containerregistry.googleapis.com"
    else
        print_warning "Failed to enable containerregistry.googleapis.com (might already be enabled)"
    fi
    
    print_success "APIs enabled successfully"
}

# Build and push Docker image
build_and_push() {
    print_status "Building and pushing Docker image..."
    
    # Check if Dockerfile exists
    if [ ! -f "Dockerfile" ]; then
        print_error "Dockerfile not found in current directory"
        exit 1
    fi
    
    # Build the image with progress
    print_status "Building Docker image: $IMAGE_NAME"
    if docker build -t "$IMAGE_NAME" .; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
    
    # Push to Container Registry
    print_status "Pushing Docker image to Container Registry..."
    if docker push "$IMAGE_NAME"; then
        print_success "Docker image pushed successfully"
    else
        print_error "Failed to push Docker image"
        exit 1
    fi
}

# Deploy to Cloud Run
deploy() {
    print_status "Deploying to Cloud Run..."
    
    # Deploy with all necessary flags
    deploy_cmd="gcloud run deploy $SERVICE_NAME \
        --image $IMAGE_NAME \
        --region $REGION \
        --platform managed \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --timeout 3600 \
        --concurrency 80 \
        --max-instances 10 \
        --set-env-vars STREAMLIT_SERVER_PORT=8080,STREAMLIT_SERVER_ADDRESS=0.0.0.0,STREAMLIT_SERVER_HEADLESS=true \
        --port 8080"
    
    print_status "Running: $deploy_cmd"
    
    if eval $deploy_cmd; then
        print_success "Deployment completed successfully"
    else
        print_error "Deployment failed"
        exit 1
    fi
}

# Set environment variables
set_environment_variables() {
    print_status "Setting environment variables..."
    
    # Read from .env file if it exists
    if [ -f ".env" ]; then
        print_status "Reading environment variables from .env file..."
        
        # Create a temporary file for valid environment variables
        temp_env_file=$(mktemp)
        
        # Filter and process .env file
        while IFS='=' read -r key value; do
            # Skip comments and empty lines
            if [ -n "$key" ] && [ "$(echo "$key" | cut -c1)" != "#" ]; then
                # Remove quotes from value
                clean_value=$(echo "$value" | sed 's/^"//;s/"$//')
                echo "$key=$clean_value" >> "$temp_env_file"
            fi
        done < .env
        
        # Set environment variables in batches
        if [ -s "$temp_env_file" ]; then
            print_status "Setting environment variables..."
            
            # Build environment variables string for single command
            env_vars=""
            while IFS='=' read -r key value; do
                if [ -n "$key" ]; then
                    if [ -z "$env_vars" ]; then
                        env_vars="$key=$value"
                    else
                        env_vars="$env_vars,$key=$value"
                    fi
                fi
            done < "$temp_env_file"
            
            # Set all environment variables in a single command
            if [ -n "$env_vars" ]; then
                print_status "Setting all environment variables in one command..."
                if gcloud run services update "$SERVICE_NAME" \
                    --region "$REGION" \
                    --update-env-vars "$env_vars" \
                    --quiet; then
                    print_success "All environment variables set successfully"
                else
                    print_warning "Failed to set environment variables"
                fi
            fi
            
            # Clean up temporary file
            rm -f "$temp_env_file"
            
            print_success "Environment variables set successfully"
        else
            print_warning "No valid environment variables found in .env file"
        fi
    else
        print_warning "No .env file found. Please set environment variables manually in the Google Cloud Console."
        print_status "Required environment variables:"
        print_status "  - OPENROUTER_API_KEY"
        print_status "  - GOOGLE_GEMINI_API_KEY"
    fi
}

# Get the service URL
get_service_url() {
    print_status "Getting service URL..."
    
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region "$REGION" \
        --format "value(status.url)")
    
    if [ -n "$SERVICE_URL" ]; then
        print_success "Service deployed successfully!"
        print_success "Service URL: $SERVICE_URL"
        echo ""
        print_status "You can now access your Neo AI Tutor application at:"
        echo -e "${GREEN}$SERVICE_URL${NC}"
    else
        print_error "Failed to get service URL"
        exit 1
    fi
}

# Main deployment function
main() {
    echo "🚀 Neo AI Tutor - Google Cloud Run Deployment"
    echo "=============================================="
    echo ""
    
    # Check if PROJECT_ID is set
    if [ "$PROJECT_ID" = "your-project-id" ]; then
        print_error "Please update the PROJECT_ID variable in this script with your actual Google Cloud project ID."
        exit 1
    fi
    
    print_status "Starting deployment with project: $PROJECT_ID"
    print_status "Region: $REGION"
    print_status "Service name: $SERVICE_NAME"
    echo ""
    
    #check_prerequisites
    authenticate
    set_project
    enable_apis
    build_and_push
    deploy
    set_environment_variables
    get_service_url
    
    echo ""
    print_success "Deployment completed! 🎉"
    print_status "Your application is now live and accessible!"
}

# Run the main function
main "$@" 