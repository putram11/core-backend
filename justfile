# Development commands for Core Backend

# Variables
set dotenv-load := true

# Default recipe - show help
default:
    @just --list

# Start development environment
up:
    docker-compose -f docker-compose.dev.yml up --build

# Start development environment in background  
dev:
    docker-compose -f docker-compose.dev.yml up --build -d
    @echo "🚀 Development environment is running!"
    @echo "📊 Django Admin: http://localhost:8000/admin"
    @echo "📋 API Docs: http://localhost:8000/api/docs/"
    @echo "📖 ReDoc: http://localhost:8000/api/redoc/"
    @echo "🔍 Health Check: http://localhost:8000/api/health/"
    @echo "🗄️  Database: localhost:5432"
    @echo "🔥 Redis: localhost:6379"
    @echo ""
    @echo "Use 'just logs' to view logs"
    @echo "Use 'just down' to stop services"

# Stop all services
down:
    docker-compose -f docker-compose.dev.yml down

# Stop and clean up everything
clean:
    docker-compose -f docker-compose.dev.yml down -v --remove-orphans
    docker system prune -f

# Build containers
build:
    docker-compose -f docker-compose.dev.yml build --no-cache

# View logs (default: web service)
logs service="web":
    docker-compose -f docker-compose.dev.yml logs -f {{service}}

# View all service logs
logs-all:
    docker-compose -f docker-compose.dev.yml logs -f

# Django management commands
manage cmd:
    docker-compose -f docker-compose.dev.yml exec web python manage.py {{cmd}}

# Run migrations (make + migrate)
migrate:
    docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations
    docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Reset database (⚠️ deletes all data)
reset-db:
    docker-compose -f docker-compose.dev.yml exec web python manage.py flush --noinput
    just migrate

# Create superuser
superuser:
    docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Django shell
shell:
    docker-compose -f docker-compose.dev.yml exec web python manage.py shell

# Container bash shell
bash:
    docker-compose -f docker-compose.dev.yml exec web bash

# Testing
test:
    docker-compose -f docker-compose.dev.yml exec web python -m pytest

# Run tests with coverage
test-cov:
    docker-compose -f docker-compose.dev.yml exec web python -m pytest --cov=. --cov-report=html --cov-report=term

# Generate OpenAPI schema
schema:
    docker-compose -f docker-compose.dev.yml exec web python manage.py spectacular --color --file schema.yml
    @echo "📋 Schema generated at schema.yml"

# Code quality
format:
    docker-compose -f docker-compose.dev.yml exec web black .
    docker-compose -f docker-compose.dev.yml exec web isort .

# Check code quality
quality:
    docker-compose -f docker-compose.dev.yml exec web black --check .
    docker-compose -f docker-compose.dev.yml exec web isort --check-only .
    docker-compose -f docker-compose.dev.yml exec web flake8 .

# Run linting only  
lint:
    docker-compose -f docker-compose.dev.yml exec web flake8 .

# Database operations
db-shell:
    docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d core_backend

# Container status
ps:
    docker-compose -f docker-compose.dev.yml ps

# Show all available commands
help:
    @just --list

# Production commands
prod-build:
    docker-compose -f docker-compose.yml build

prod-up:
    docker-compose -f docker-compose.yml up -d

prod-down:
    docker-compose -f docker-compose.yml down

# Install pre-commit hooks
install-hooks:
    pre-commit install
    pre-commit install --hook-type commit-msg

# Run pre-commit on all files
pre-commit:
    pre-commit run --all-files
