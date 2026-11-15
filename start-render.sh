#!/bin/sh
set -eu

exec gunicorn \
  --bind "0.0.0.0:${PORT:-10000}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  app:app
