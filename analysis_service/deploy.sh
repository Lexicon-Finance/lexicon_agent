#!/bin/bash

# Exit on any error
set -e

# Configuration
PROJECT_ID="lexicon-agent"    # Same project ID
REGION="europe-west1"         # Same region
SERVICE_NAME="analysis-service"
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
  --port 8001 \
  --set-secrets="OPENAI_API_KEY=OPENAI_API_KEY:latest,\
TENDERLY_API_KEY=TENDERLY_API_KEY:latest,\
ETHERSCAN_API_KEY=ETHERSCAN_API_KEY:latest,\
LANGSMITH_API_KEY=LANGSMITH_API_KEY:latest,\
OWNER_A_PRIVATE_KEY=OWNER_A_PRIVATE_KEY:latest" \
  --set-env-vars="LANGSMITH_TRACING=true,\
LANGSMITH_ENDPOINT=https://api.smith.langchain.com,\
LANGSMITH_PROJECT=pr-mundane-landing-37,\
RPC_URL=https://eth-sepolia.public.blastapi.io,\
ETHERSCAN_URL=https://api-sepolia.etherscan.io/api,\
SAFE_ADDRESS=0x179a8BDDa1AB5fEF17AAF6Ff0FFCb2875925668F"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)')

echo "✅ Deployment complete!"
echo "🌍 Service URL: $SERVICE_URL"
echo "🔍 To view logs: gcloud run services logs read $SERVICE_NAME --region $REGION" 