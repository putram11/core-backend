# Core Backend Development Commands

# Set up and run the development environment
up:
    docker-compose -f docker-compose.dev.yml up --build -d
    @echo "🚀 Development environment is running at http://localhost:8000"
    @echo "📊 Admin panel: http://localhost:8000/admin"
    @echo "� API Docs (Swagger): http://localhost:8000/api/docs/"
    @echo "📖 API Docs (ReDoc): http://localhost:8000/api/redoc/"
    @echo "🔍 Health Check: http://localhost:8000/api/health/"
    @echo "�🗄️  PostgreSQL: localhost:5432"
    @echo "🔥 Redis: localhost:6379"

# Stop all services
down:
    docker-compose -f docker-compose.dev.yml down

# View logs
logs service="web":
    docker-compose -f docker-compose.dev.yml logs -f {{service}}

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

# Check import sorting
check-imports:
    docker-compose -f docker-compose.dev.yml exec web isort --check-only .

# Sort imports
sort-imports:
    docker-compose -f docker-compose.dev.yml exec web isort .

# Run all quality checks
quality: check-format check-imports lint

# Open shell in web container
shell:
    docker-compose -f docker-compose.dev.yml exec web python manage.py shell

# Open bash in web container
bash:
    docker-compose -f docker-compose.dev.yml exec web bash

# Reset database (WARNING: This will delete all data)
reset-db:
    docker-compose -f docker-compose.dev.yml down
    docker volume rm core-backend_postgres_data || true
    just up
    just migrate
    @echo "🗑️  Database reset complete"

# Backup database
backup:
    docker-compose -f docker-compose.dev.yml exec db pg_dump -U postgres core_backend_dev > backup_$(date +%Y%m%d_%H%M%S).sql
    @echo "💾 Database backed up"

# Show running services
ps:
    docker-compose -f docker-compose.dev.yml ps

# Restart specific service
restart service:
    docker-compose -f docker-compose.dev.yml restart {{service}}

# Build without cache
build:
    docker-compose -f docker-compose.dev.yml build --no-cache

# Clean up unused Docker resources
clean:
    docker system prune -f
    docker volume prune -f

# Show help
help:
    @echo "🚀 Core Backend Development Commands"
    @echo ""
    @echo "Main commands:"
    @echo "  just up           - Start development environment"
    @echo "  just down         - Stop all services"
    @echo "  just logs [service] - View logs (default: web)"
    @echo ""
    @echo "Development:"
    @echo "  just migrate      - Run database migrations"
    @echo "  just superuser    - Create superuser"
    @echo "  just shell        - Open Django shell"
    @echo "  just bash         - Open bash in web container"
    @echo ""
    @echo "Testing & Quality:"
    @echo "  just test         - Run tests"
    @echo "  just test-coverage - Run tests with coverage"
    @echo "  just quality      - Run all quality checks"
    @echo "  just format       - Format code with black"
    @echo "  just lint         - Run flake8 linting"
    @echo ""
    @echo "Utilities:"
    @echo "  just reset-db     - Reset database (⚠️  deletes all data)"
    @echo "  just backup       - Backup database"
    @echo "  just clean        - Clean up Docker resources"
