#!/bin/sh
set -e

# Ensure runtime directories exist
mkdir -p /app/media /app/logs /app/static

# Try to fix ownership if possible
if [ "$(id -u)" = "0" ]; then
  echo "🧰 Running as root, fixing ownership..."
  for dir in /app/media /app/logs /app/static; do
    if [ -d "$dir" ]; then
      chown -R django:django "$dir" || true
    else
      echo "⚠️ Directory $dir not found, skipping..."
    fi
  done
else
  echo "⚠️ Not root, skipping chown (permissions must be correct on host)"
fi

# Execute the provided command
exec "$@"
