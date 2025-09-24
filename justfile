# Core Backend Development Commands

# Set up and run the development environment with logs
up:
    docker-compose -f docker-compose.dev.yml up --build -d
    @echo "🚀 Development environment is running at http://localhost:8000"
    @echo "📊 Admin panel: http://localhost:8000/admin"
    @echo "📋 API Docs (Swagger): http://localhost:8000/api/docs/"
    @echo "📖 API Docs (ReDoc): http://localhost:8000/api/redoc/"
    @echo "🔍 Health Check: http://localhost:8000/api/health/"
    @echo "🗄️  PostgreSQL: localhost:5432"
    @echo "🔥 Redis: localhost:6379"
    @echo ""
    @echo "📄 Showing logs (Ctrl+C to stop watching logs):"
    @sleep 3
    docker-compose -f docker-compose.dev.yml logs -f web

# Stop all services
down:
    docker-compose -f docker-compose.dev.yml down

# Build without running
build:
    docker-compose -f docker-compose.dev.yml build --no-cache

# View logs
logs service="web":
    docker-compose -f docker-compose.dev.yml logs -f {{service}}

# View all logs (web, db, redis)
logs-all:
    docker-compose -f docker-compose.dev.yml logs -f

# Run Django management commands
manage cmd:
    docker-compose -f docker-compose.dev.yml exec web python manage.py {{cmd}}

# Create and run migrations
migrate:
    docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations
    docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Create superuser
superuser:
    docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Generate OpenAPI schema
schema:
    docker-compose -f docker-compose.dev.yml exec web python manage.py spectacular --color --file schema.yml
    @echo "📋 Schema generated at schema.yml"

# Run tests
test:
    docker-compose -f docker-compose.dev.yml exec web python manage.py test

# Run tests with coverage
test-coverage:
    docker-compose -f docker-compose.dev.yml exec web coverage run --source='.' manage.py test
    docker-compose -f docker-compose.dev.yml exec web coverage report
    docker-compose -f docker-compose.dev.yml exec web coverage html

# Format code with black
format:
    docker-compose -f docker-compose.dev.yml exec web black .

# Check code formatting
check-format:
    docker-compose -f docker-compose.dev.yml exec web black --check .

# Run linting
lint:
    docker-compose -f docker-compose.dev.yml exec web flake8 .

# Check imports
check-imports:
    docker-compose -f docker-compose.dev.yml exec web isort --check-only .

# Fix imports
fix-imports:
    docker-compose -f docker-compose.dev.yml exec web isort .

# Run all quality checks
quality-check:
    just check-format
    just check-imports
    just lint
    just test

# Clean up containers and images
clean:
    docker-compose -f docker-compose.dev.yml down -v
    docker system prune -f

# Enter web container shell
shell:
    docker-compose -f docker-compose.dev.yml exec web bash

# Enter postgres shell
db-shell:
    docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d core_backend

# Run production build
build-prod:
    docker-compose -f docker-compose.prod.yml build

# Backup database
backup:
    mkdir -p backups
    docker-compose -f docker-compose.dev.yml exec db pg_dump -U postgres core_backend > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database from backup
restore file:
    docker-compose -f docker-compose.dev.yml exec db psql -U postgres core_backend < {{file}}

# Show container status
status:
    docker-compose -f docker-compose.dev.yml ps

# Show resource usage
stats:
    docker stats

# Update dependencies
update-deps:
    pip-compile requirements.in
    pip-compile requirements-dev.in
