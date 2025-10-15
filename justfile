export COMPOSE_FILE := "docker-compose.dev.yml"

## Just does not yet manage signals for subprocesses reliably, which can lead to unexpected behavior.
## Exercise caution before expanding its usage in production environments.
## For more information, see https://github.com/casey/just/issues/2473 .

# Default command to list all available commands.
default:
    @just --list

# build: Build python image.
build:
    @echo "Building python image..."
    @docker compose build

# up: Start up containers.
up:
    @echo "Starting up containers..."
    @docker compose up --remove-orphans

# down: Stop containers.
down:
    @echo "Stopping containers..."
    @docker compose down

# prune: Remove containers and their volumes.
prune *args:
    @echo "Killing containers and removing volumes..."
    @docker compose down -v {{args}}

# logs: View container logs
logs *args:
    @docker compose logs -f {{args}}

# django: Run a command in the Django container.
django +args:
    @docker compose run --rm web {{args}}

# manage: Executes `manage.py` command.
manage +args:
    @docker compose run --rm web python ./manage.py {{args}}

# shell: Run bash shell in Django container.
shell:
    @docker compose run --rm web bash

# django-shell: Run Django shell.
django-shell:
    @docker compose run --rm web python manage.py shell

# test: Run tests.
test:
    @docker compose run --rm web python manage.py test

# lint: Check code with flake8.
lint:
    @docker compose run --rm web flake8 .

# collectstatic: Collect static files.
collectstatic:
    @docker compose run --rm web python manage.py collectstatic --noinput

# Create superuser
createsuperuser:
    @docker compose run --rm web python manage.py createsuperuser

# Format code with black
format:
    @docker compose run --rm web black .

# Check code formatting
check-format:
    @docker compose run --rm web black --check .

# Check imports
check-imports:
    @docker compose run --rm web isort --check-only .

# Fix imports
fix-imports:
    @docker compose run --rm web isort .

# migrations: Run Django migrations
migrations:
    @echo "🚀 Running migrations..."
    @docker compose run --rm web python manage.py migrate

# makemigrations: Create new migrations
makemigrations *args:
    @echo "📝 Creating migrations..."
    @docker compose run --rm web python manage.py makemigrations {{args}}

# showmigrations: Show migration status
showmigrations:
    @echo "📋 Migration status:"
    @docker compose run --rm web python manage.py showmigrations

# migrate-zero: Reset migrations to zero state
migrate-zero app:
    @echo "⏪ Resetting {{app}} migrations to zero..."
    @docker compose run --rm web python manage.py migrate {{app}} zero

# Generate OpenAPI schema
schema:
    @docker compose run --rm web python manage.py spectacular --color --file schema.yml
    @echo "📋 Schema generated at schema.yml"

# Run tests with coverage
test-coverage:
    @docker compose run --rm web coverage run --source='.' manage.py test
    @docker compose run --rm web coverage report
    @docker compose run --rm web coverage html

# Run all quality checks
quality-check:
    just check-format
    just check-imports
    just lint
    just test

# Clean up containers and images
clean:
    @docker compose down -v
    @docker system prune -f

# Show container status
status:
    @docker compose ps

# Show resource usage
stats:
    @docker stats

# Enter postgres shell (need running container)
db-shell:
    @docker compose exec db psql -U postgres -d core_backend_dev

# Reset database (drop and recreate with migrations)
reset-db:
    @echo "🗑️  Dropping database..."
    @docker compose exec db dropdb -U postgres --if-exists core_backend_dev
    @echo "🔨 Creating fresh database..."
    @docker compose exec db createdb -U postgres core_backend_dev
    @echo "🚀 Running migrations..."
    @docker compose run --rm web python manage.py migrate
    @echo "✅ Database reset complete!"

# reset: Reset database and start fresh (shortcut)
reset:
    @echo "🔄 Resetting everything..."
    @docker compose down -v
    @docker compose up -d db redis
    @sleep 3
    @echo "🚀 Running migrations..."
    @docker compose run --rm web python manage.py migrate
    @echo "✅ Reset complete! Use 'just up' to start all services."

# Backup database
backup:
    @mkdir -p backups
    @docker compose exec db pg_dump -U postgres core_backend_dev > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database from backup
restore file:
    @docker compose exec db psql -U postgres core_backend_dev < {{file}}

# Install pre-commit hooks
install-hooks:
    @pre-commit install
    @pre-commit install --hook-type commit-msg

# Run pre-commit on all files
pre-commit:
    @pre-commit run --all-files

# ----------------------------
# Production helpers (use .env.production)
# ----------------------------

# Helper: run a command with environment loaded from .env.production
with-prod +cmd:
    @echo "Loading .env.production and running: {{cmd}}"
    @set -a; [ -f .env.production ] && . .env.production || true; set +a; \
    docker compose -f docker-compose.prod.web.yml {{cmd}}

# Start production services (detached)
prod-up:
    @echo "Starting production services (using .env.production)..."
    @just with-prod up -d

# Stop production services
prod-down:
    @echo "Stopping production services..."
    @just with-prod down

# View production logs
prod-logs *args:
    @just with-prod logs --tail=200 {{args}}

# Run a manage.py command in production (via docker compose run)
prod-manage +args:
    @echo "Running manage.py in production: {{args}}"
    @set -a; [ -f .env.production ] && . .env.production || true; set +a; \
    docker compose -f docker-compose.prod.web.yml run --rm web python manage.py {{args}}

# Run migrations in production
prod-migrate:
    @echo "Running migrations in production..."
    @just prod-manage migrate

# Collect static in production
prod-collectstatic:
    @echo "Collecting static files in production..."
    @just prod-manage collectstatic --noinput

# Open shell in production web container
prod-shell:
    @set -a; [ -f .env.production ] && . .env.production || true; set +a; \
    docker compose -f docker-compose.prod.web.yml run --rm web bash
