#!/usr/bin/env bash

set -euo pipefail

echo "Checking configuration..."
docker compose config --quiet

echo "Building and starting the application..."
docker compose up -d --build --wait

echo "Checking that the app can reach MongoDB..."
docker compose exec -T app sh -c 'curl -f "http://localhost:${PORT}/readyz"'

echo "Deployment complete."