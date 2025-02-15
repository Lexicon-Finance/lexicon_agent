#!/bin/bash

# Exit on any error
set -e

SERVICE_NAME="safe-service"
LOCAL_PORT=8000

echo "🚀 Testing $SERVICE_NAME locally with Docker..."

# Build the container image
echo "📦 Building container image..."
docker build -t $SERVICE_NAME .

# Check if container is already running and stop it
if docker ps -q -f name=$SERVICE_NAME; then
    echo "🛑 Stopping existing container..."
    docker stop $SERVICE_NAME
    docker rm $SERVICE_NAME
fi

# Run the container
echo "🚀 Starting container..."
docker run -d \
    --name $SERVICE_NAME \
    -p $LOCAL_PORT:8000 \
    -e OWNER_A_PRIVATE_KEY="$(grep OWNER_A_PRIVATE_KEY .env | cut -d '=' -f2)" \
    -e RPC_URL="$(grep RPC_URL .env | cut -d '=' -f2)" \
    $SERVICE_NAME

echo "✅ Local deployment complete!"
echo "🌍 Service URL: http://localhost:$LOCAL_PORT"
echo "📝 To view logs: docker logs $SERVICE_NAME"
echo "🛑 To stop: docker stop $SERVICE_NAME" 