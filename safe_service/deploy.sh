#!/bin/bash

# Exit on any error
set -e

# Configuration
PROJECT_ID="lexicon-agent"  # Replace with your Google Cloud project ID
REGION="europe-west1"         # Your current region
SERVICE_NAME="safe-service"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying $SERVICE_NAME to Google Cloud Run..."

# Build the container image
echo "📦 Building container image..."
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000 \
  --set-secrets="OWNER_A_PRIVATE_KEY=OWNER_A_PRIVATE_KEY:latest" \
  --set-env-vars="RPC_URL=https://eth-sepolia.public.blastapi.io"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)')

echo "✅ Deployment complete!"
echo "🌍 Service URL: $SERVICE_URL"
echo "🔍 To view logs: gcloud run services logs read $SERVICE_NAME --region $REGION" 