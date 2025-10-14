#!/bin/bash
# Production deployment script for Django web service only
# 
# Prerequisites:
# - PostgreSQL and Redis running on host
# - .env file configured with correct DATABASE_URL and REDIS_URL
# - Nginx configured to proxy to this service

set -e

echo "🚀 Starting production deployment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found! Copy .env.example to .env and configure it."
    exit 1
fi

# Source environment variables
source .env

echo "📦 Building production image..."
docker compose -f docker-compose.prod.web.yml build

echo "🗃️  Running database migrations..."
docker compose -f docker-compose.manage.yml run --rm manage migrate

echo "📁 Collecting static files..."
docker compose -f docker-compose.manage.yml run --rm manage collectstatic --noinput

echo "🔧 Starting web service..."
docker compose -f docker-compose.prod.web.yml up -d

echo "⏳ Waiting for service to be ready..."
sleep 10

# Check if service is running
if docker compose -f docker-compose.prod.web.yml ps | grep -q "Up"; then
    echo "✅ Deployment successful!"
    echo "🌐 Service running on port ${WEB_PORT:-8000}"
    echo "📊 Check logs: docker compose -f docker-compose.prod.web.yml logs -f"
    echo "🔄 Update: ./scripts/deploy.sh"
    echo "🛑 Stop: docker compose -f docker-compose.prod.web.yml down"
else
    echo "❌ Deployment failed! Check logs:"
    docker compose -f docker-compose.prod.web.yml logs
    exit 1
fi