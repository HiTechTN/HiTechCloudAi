.PHONY: help install build start stop restart logs clean test lint format

help:
	@echo "Blink.local - Available Commands"
	@echo "================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install              Install dependencies and setup"
	@echo "  make build                Build Docker images"
	@echo ""
	@echo "Running Services:"
	@echo "  make start                Start all services"
	@echo "  make stop                 Stop all services"
	@echo "  make restart              Restart all services"
	@echo ""
	@echo "Development:"
	@echo "  make logs                 View logs from all services"
	@echo "  make logs-backend         View backend logs"
	@echo "  make logs-frontend        View frontend logs"
	@echo "  make shell-backend        Open Django shell"
	@echo "  make migrate              Run Django migrations"
	@echo "  make createsuperuser      Create admin user"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint                 Run linters"
	@echo "  make format               Format code"
	@echo "  make test                 Run tests"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean                Remove containers & volumes"
	@echo "  make fresh                Clean rebuild everything"
	@echo "  make env                  Generate .env file"
	@echo "  make tunnel               Setup Cloudflare tunnel"
	@echo "  make pull-models          Pull Ollama models"
	@echo ""

install: env build
	@echo "Installation complete!"
	@echo "Run 'make start' to launch services"

env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please update with your credentials."; \
	else \
		echo ".env already exists"; \
	fi

build:
	docker-compose build

start:
	docker-compose up -d
	@echo "Services starting... Check with 'make logs'"
	@sleep 5
	@make status

stop:
	docker-compose down

restart: stop start

status:
	@docker-compose ps

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-nginx:
	docker-compose logs -f nginx

shell-backend:
	docker-compose exec backend python manage.py shell

migrate:
	docker-compose exec backend python manage.py migrate

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

lint:
	docker-compose exec backend flake8 .
	npm run lint

format:
	docker-compose exec backend black .
	npm run format

test:
	docker-compose exec backend pytest
	npm test

clean:
	docker-compose down -v
	@echo "Containers and volumes removed"

fresh: clean build start
	@echo "Fresh installation complete!"

tunnel:
	bash scripts/setup-cloudflare.sh

pull-models:
	docker-compose exec ollama ollama pull codellama
	docker-compose exec ollama ollama pull mistral

health-check:
	@echo "Checking service health..."
	@curl -s http://localhost:8000/api/health/ | jq . || echo "Backend: NOT RESPONDING"
	@curl -s http://localhost/health || echo "Nginx: NOT RESPONDING"
	@echo "Frontend: http://localhost:5173"
	@echo "Code-Server: https://localhost:8443"

stats:
	docker stats

backup-db:
	@mkdir -p backups
	@docker-compose exec -T backend pg_dump \
		-h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) \
		> backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backups/"

restore-db:
	@if [ ! -f $(FILE) ]; then \
		echo "FILE not specified. Usage: make restore-db FILE=backups/backup_*.sql"; \
		exit 1; \
	fi
	@docker-compose exec -T backend psql \
		-h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) < $(FILE)
	@echo "Database restored from $(FILE)"

update-deps:
	docker-compose exec backend pip install --upgrade -r requirements.txt
	npm update

production-build:
	npm run build
	docker-compose build --no-cache

ps:
	docker-compose ps

exec-backend:
	docker-compose exec backend bash

exec-frontend:
	docker-compose exec frontend bash
