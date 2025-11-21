#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}--- Tearing down existing services to ensure a clean state ---${NC}"
docker-compose down -v

echo -e "\n${GREEN}--- Building and starting services ---${NC}"
docker-compose up -d --build

echo -e "\n${GREEN}--- Running Backend Tests (pytest) ---${NC}"
docker-compose exec backend pytest

echo -e "\n${GREEN}--- Setting up Frontend for E2E Tests ---${NC}"
# Navigate to the frontend directory to run npm commands
cd frontend

# Install npm dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
  echo "node_modules not found, running npm install..."
  npm install
fi

# Install Playwright browsers and their dependencies
echo "Installing Playwright browsers..."
npx playwright install --with-deps

echo -e "\n${GREEN}--- Running Frontend E2E Tests (Playwright) ---${NC}"
npx playwright test

# Navigate back to the root
cd ..

echo -e "\n${GREEN}All tests passed successfully!${NC}"