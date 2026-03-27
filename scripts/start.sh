#!/bin/bash

set -e

echo "Starting Blink.local Clone..."
echo "============================="

if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cat > .env << 'EOF'
DJANGO_SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=*

SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
SUPABASE_DB_URL=your-supabase-db-url

DB_NAME=blink
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432

REDIS_URL=redis://redis:6379/0
OLLAMA_API_URL=http://ollama:11434

CODE_SERVER_PASSWORD=password123
CLOUDFLARE_TUNNEL_TOKEN=your-cloudflare-tunnel-token
EOF
    echo ".env file created. Please update it with your credentials."
fi

echo "Building Docker images..."
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

echo ""
echo "Checking service health..."
echo ""

services=("backend" "frontend" "nginx" "redis" "code-server")

for service in "${services[@]}"; do
    if docker-compose ps $service | grep -q "Up"; then
        echo "✓ $service is running"
    else
        echo "✗ $service is not running"
    fi
done

echo ""
echo "========================================"
echo "Blink.local is starting!"
echo "========================================"
echo ""
echo "Frontend:   http://localhost:80 (via nginx)"
echo "API:        http://localhost:8000/api/"
echo "Code-Server: http://localhost:8443"
echo ""
echo "To setup Cloudflare Tunnel for external access:"
echo "  bash scripts/setup-cloudflare.sh"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
