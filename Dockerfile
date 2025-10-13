FROM python:3.11-slim

# Build argument for development mode
ARG DEV=false

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        postgresql-client \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Create user for non-root execution
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install development dependencies if DEV=true
COPY requirements-dev.txt .
RUN if [ "$DEV" = "true" ]; then \
        pip install --no-cache-dir -r requirements-dev.txt; \
    fi

# Copy project
COPY . .

# Create directories and change ownership
RUN mkdir -p /app/static /app/media /app/logs \
    && chown -R django:django /app

# Collect static files (for production)
RUN if [ "$DEV" != "true" ]; then \
        python manage.py collectstatic --noinput; \
    fi

# Switch to django user
USER django

# Expose port
EXPOSE 8000

# Default command
CMD if [ "$DEV" = "true" ]; then \
        python manage.py runserver 0.0.0.0:8000; \
    else \
        gunicorn --bind 0.0.0.0:8000 --workers 3 core.wsgi:application; \
    fi
