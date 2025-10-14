#!/bin/sh
set -e

# Ensure runtime directories exist and are writable by the django user
mkdir -p /app/media /app/logs /app/static
chown -R django:django /app/media /app/logs /app/static || true

# Execute the provided command
exec "$@"
