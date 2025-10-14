#!/bin/bash
# Production deployment script for Django web service only
# 
# Prerequisites:
# - PostgreSQL and Redis running on host
# - .env file configured with correct DATABASE_URL and REDIS_URL
# - Nginx configured to proxy to this service

set -e

echo "🚀 Starting production deployment for api-corebackend.kancralabs.com..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Creating .env from template..."
    if [ -f .env.production ]; then
        cp .env.production .env
        echo "✅ Copied .env.production to .env"
        echo "⚠️  Please edit .env and update:"
        echo "   - SECRET_KEY (generate new one)"
        echo "   - DATABASE_URL (your postgres credentials)"
        echo "   - REDIS_URL (if using auth)"
        echo "   - EMAIL_* settings (if needed)"
        echo ""
        echo "🔐 Generate SECRET_KEY with:"
        echo "   python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
        exit 1
    else
        echo "❌ No .env.production template found!"
        exit 1
    fi
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
    echo "🔗 URL: https://api-corebackend.kancralabs.com"
    echo "📊 Check logs: docker compose -f docker-compose.prod.web.yml logs -f"
    echo "🔄 Update: ./scripts/deploy.sh"
    echo "🛑 Stop: docker compose -f docker-compose.prod.web.yml down"
    echo ""
    echo "🔧 Don't forget to configure nginx to:"
    echo "   - Proxy requests to localhost:${WEB_PORT:-8000}"
    echo "   - Serve static files from ./static/"
    echo "   - Serve media files from ./media/"
    echo "   - Set proper SSL headers"
else
    echo "❌ Deployment failed! Check logs:"
    docker compose -f docker-compose.prod.web.yml logs
    exit 1
fi