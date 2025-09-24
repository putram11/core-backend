# Core Backend - Django REST API

A modern Django REST API backend with JWT authentication, Docker containerization, and CI/CD pipeline.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👤 **Custom User Model** - Extended user model with additional fields
- � **Swagger Documentation** - Interactive API documentation with OpenAPI 3.0
- �🐳 **Docker Support** - Full containerization with Docker Compose
- 🧪 **Testing** - Comprehensive test suite with pytest
- 🚀 **CI/CD Pipeline** - GitHub Actions for automated testing and deployment
- 🔄 **Celery Integration** - Background task processing
- 💾 **Redis Caching** - Fast caching layer
- 🗄️ **PostgreSQL** - Production-ready database
- 🛡️ **Security** - Security best practices implemented

## Tech Stack

- **Backend**: Django 5.1+, Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **Cache**: Redis
- **Task Queue**: Celery
- **Authentication**: JWT (Simple JWT)
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Code Quality**: Black, Flake8, isort

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Just](https://github.com/casey/just) command runner (`brew install just` on macOS)

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/putram11/core-backend.git
   cd core-backend
   ```

2. **Start the development environment:**
   ```bash
   just up
   ```
   
   This command will:
   - Build the Docker containers
   - Start PostgreSQL, Redis, and Django services
   - Run database migrations
   - Make the API available at http://localhost:8000

3. **Create a superuser:**
   ```bash
   just superuser
   ```

4. **Access the application:**
   - **API:** http://localhost:8000/api/
   - **Admin Panel:** http://localhost:8000/admin/
   - **API Health Check:** http://localhost:8000/api/health/

### Development Commands

```bash
# Start development environment
just up

# Stop all services
just down

# View logs
just logs        # web service logs
just logs db     # database logs

# Database operations
just migrate     # Run migrations
just reset-db    # Reset database (⚠️ deletes all data)

# Development tools
just shell       # Django shell
just bash        # Container bash
just superuser   # Create superuser

# Testing and code quality
just test        # Run tests
just quality     # Run all quality checks
just format      # Format code with Black

# View all available commands
just help
```

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for development

# Setup environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

#### Option B: Docker Development

```bash
# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web
```

### 3. Access the Application

- **API Base URL**: http://localhost:8000/api/
- **Swagger Documentation**: http://localhost:8000/api/docs/
- **ReDoc Documentation**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/api/health/

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | User registration | No |
| POST | `/api/auth/login/` | User login | No |
| POST | `/api/auth/logout/` | User logout | Yes |
| POST | `/api/auth/token/refresh/` | Refresh JWT token | No |
| GET | `/api/auth/profile/` | Get user profile | Yes |
| PUT | `/api/auth/profile/` | Update user profile | Yes |
| POST | `/api/auth/change-password/` | Change password | Yes |
| GET | `/api/auth/me/` | Get current user info | Yes |

### General

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/` | API information | No |
| GET | `/api/health/` | Health check | No |

## API Documentation

The API is fully documented using **Swagger UI** and **ReDoc**:

- **Swagger UI**: http://localhost:8000/api/docs/ - Interactive API documentation
- **ReDoc**: http://localhost:8000/api/redoc/ - Clean, responsive API documentation
- **OpenAPI Schema**: http://localhost:8000/api/schema/ - Raw OpenAPI 3.0 schema

### Features:
- Interactive API testing directly in the browser
- JWT authentication support in Swagger UI
- Comprehensive request/response examples
- Auto-generated from Django REST Framework serializers
- OpenAPI 3.0 compliant

### Generate Schema File
```bash
just schema
# or manually:
docker-compose -f docker-compose.dev.yml exec web python manage.py spectacular --color --file schema.yml
```

## Project Structure

```
core-backend/
├── core/                   # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── users/                 # User management app
│   ├── models.py          # Custom User model
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── urls.py            # App URLs
│   └── admin.py           # Admin configuration
├── api/                   # General API app
│   ├── views.py           # General API views
│   └── urls.py            # API URLs
├── tests/                 # Test files
│   └── test_authentication.py
├── scripts/               # Utility scripts
│   └── setup.sh           # Setup script
├── nginx/                 # Nginx configuration
│   └── nginx.conf
├── .github/               # GitHub Actions workflows
│   └── workflows/
│       ├── ci-cd.yml      # Main CI/CD pipeline
│       └── deploy.yml     # Deployment workflow
├── docker-compose.yml     # Docker Compose for production
├── docker-compose.dev.yml # Docker Compose for development
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
├── requirements-dev.txt   # Development dependencies
├── .env.example           # Environment variables template
├── .dockerignore          # Docker ignore file
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-very-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
DATABASE_URL=postgres://user:password@localhost:5432/database_name

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Docker Commands

### Development

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# Build and start
docker-compose -f docker-compose.dev.yml up --build

# Stop services
docker-compose -f docker-compose.dev.yml down

# View logs
docker-compose -f docker-compose.dev.yml logs -f web
```

### Production

```bash
# Start all services
docker-compose up -d

# Build and start with Nginx
docker-compose --profile production up -d

# Stop services
docker-compose down
```

### Useful Docker Commands

```bash
# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Database shell
docker-compose exec db psql -U postgres -d core_backend

# Redis CLI
docker-compose exec redis redis-cli
```

## Development

### Running Tests

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Run specific test file
python manage.py test tests.test_authentication
```

### Code Quality

```bash
# Format code with Black
black .

# Check import sorting
isort --check-only .
isort .  # to fix

# Lint with flake8
flake8 .
```

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (if fixtures exist)
python manage.py loaddata fixtures/sample_data.json
```

## Authentication Examples

### Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/register/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "user@example.com",
    "username": "newuser",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Access protected endpoint

```bash
curl -X GET http://localhost:8000/api/auth/profile/ \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Deployment

### GitHub Actions

The project includes comprehensive CI/CD pipelines:

1. **CI Pipeline** (`.github/workflows/ci-cd.yml`):
   - Runs tests with PostgreSQL and Redis
   - Code quality checks (Black, Flake8, isort)
   - Security scanning
   - Builds and pushes Docker images

2. **Deployment Pipeline** (`.github/workflows/deploy.yml`):
   - Deploys to production server
   - Runs health checks
   - Sends notifications

### Required GitHub Secrets

```bash
# Docker Hub
DOCKER_USERNAME
DOCKER_PASSWORD

# Server deployment
HOST
USERNAME
SSH_KEY
PORT
APP_URL

# Notifications (optional)
SLACK_WEBHOOK_URL
```

### Production Deployment

1. **Server Setup**:
   ```bash
   # Install Docker and Docker Compose
   # Clone repository
   # Set up environment variables
   ```

2. **Deploy**:
   ```bash
   docker-compose up -d --build
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py collectstatic --noinput
   ```

## Monitoring and Logging

- **Health Check**: `/api/health/`
- **Logs**: Available via `docker-compose logs`
- **Admin Interface**: `/admin/` for user management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## Security

- JWT tokens for authentication
- CORS properly configured
- Security headers implemented
- Environment variables for sensitive data
- Regular dependency updates via Dependabot

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check existing [Issues](https://github.com/putram11/core-backend/issues)
2. Create a new issue with detailed information
3. Join our community discussions

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

---

Built with ❤️ using Django and Docker
