#!/bin/sh
set -e

# Ensure runtime directories exist
mkdir -p /app/media /app/logs /app/static

# Try to fix ownership if possible
if [ "$(id -u)" = "0" ]; then
  echo "🧰 Running as root, fixing ownership..."
  chown -R django:django /app/media /app/logs /app/static || true
else
  echo "⚠️ Not root, skipping chown (permissions must be correct on host)"
fi

# Execute the provided command
exec "$@"
