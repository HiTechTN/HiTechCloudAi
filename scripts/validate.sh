#!/bin/bash

set -e

echo "Blink.local Project Structure Validation"
echo "========================================"
echo ""

ERRORS=0
WARNINGS=0

check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "✗ MISSING: $1"
        ((ERRORS++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✓ Directory: $1"
    else
        echo "✗ MISSING: $1"
        ((ERRORS++))
    fi
}

check_optional() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "⚠ Optional: $1"
        ((WARNINGS++))
    fi
}

echo "Configuration Files:"
check_file ".env.example"
check_optional ".env"
check_file "docker-compose.yml"
check_file ".gitignore"

echo ""
echo "Backend (Django):"
check_file "backend/requirements.txt"
check_file "backend/Dockerfile"
check_file "backend/project/settings.py"
check_file "backend/project/urls.py"
check_file "backend/project/wsgi.py"
check_file "backend/project/asgi.py"
check_file "backend/apps/core/models.py"
check_file "backend/apps/api/views.py"
check_file "backend/apps/api/serializers.py"
check_file "backend/apps/api/services.py"
check_file "backend/apps/api/urls.py"
check_file "backend/manage.py"

echo ""
echo "Frontend (React):"
check_file "src/App.tsx"
check_file "src/types/index.ts"
check_file "src/services/api.ts"
check_file "src/components/Editor.tsx"
check_file "src/components/FileTree.tsx"
check_file "src/components/OutputPanel.tsx"
check_file "src/components/AIPanel.tsx"
check_file "frontend/Dockerfile"

echo ""
echo "Nginx & Reverse Proxy:"
check_file "nginx/Dockerfile"
check_file "nginx/nginx.conf"

echo ""
echo "Configuration & Scripts:"
check_file "scripts/start.sh"
check_file "scripts/setup-cloudflare.sh"
check_file "scripts/validate.sh"
check_optional "code-server-config/settings.json"
check_optional "Makefile"

echo ""
echo "Documentation:"
check_file "README.md"
check_file "BLINK_SETUP.md"

echo ""
echo "========================================"
echo "Validation Results:"
echo "========================================"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✓ All required files are present!"
    echo ""
    echo "Next steps:"
    echo "1. Update .env with your credentials"
    echo "2. Run: bash scripts/start.sh"
    echo "3. Open http://localhost in your browser"
    exit 0
else
    echo "✗ Missing files detected. Please check above."
    exit 1
fi
