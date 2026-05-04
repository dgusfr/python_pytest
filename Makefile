.PHONY: help docker-up docker-down docker-logs env-setup install serve test clean

help:
	@echo "Burguer App - Comandos disponíveis:"
	@echo ""
	@echo "  make install       - Sincronizar workspace uv"
	@echo "  make docker-up     - Subir MongoDB local"
	@echo "  make docker-down   - Parar MongoDB"
	@echo "  make docker-logs   - Ver logs do MongoDB"
	@echo "  make env-setup     - Copiar .env.example para .env"
	@echo "  make serve         - Subir todos os 4 serviços (Windows: use terminais separados)"
	@echo "  make test          - Rodar testes do auth-service"
	@echo "  make clean         - Limpar Docker volumes e venv"
	@echo ""
	@echo "Fluxo recomendado:"
	@echo "  1. make env-setup"
	@echo "  2. make docker-up"
	@echo "  3. make install"
	@echo "  4. make serve (cada serviço em um terminal)"

env-setup:
	@if not exist .env (copy .env.example .env & echo ".env criado com sucesso") else echo ".env já existe"

install:
	@echo "Sincronizando workspace uv..."
	uv sync

docker-up:
	@echo "Subindo MongoDB local..."
	docker compose up -d mongodb
	@echo "Aguardando MongoDB ficar pronto..."
	@for /l %%i in (1,1,30) do (docker exec burguer-mongodb mongosh --quiet --eval "db.version()" >nul 2>&1 && echo "MongoDB está pronto!" && exit /b 0 || (if %%i lss 30 timeout /t 1 /nobreak > nul))
	@echo "MongoDB pronto na porta 27017"

docker-down:
	@echo "Parando MongoDB..."
	docker compose stop mongodb

docker-logs:
	docker compose logs -f mongodb

docker-clean:
	@echo "Removendo MongoDB container e volumes..."
	docker compose down -v
	docker image rm mongo:7.0 2>nul || true

serve-auth:
	@echo "Iniciando auth-service na porta 5000..."
	uv run --package auth-service python burguer-app/auth-service/app.py

serve-user:
	@echo "Iniciando user-service na porta 5001..."
	uv run --package user-service python burguer-app/user-service/app.py

serve-order:
	@echo "Iniciando order-service na porta 5002..."
	uv run --package order-service python burguer-app/order-service/app.py

serve-product:
	@echo "Iniciando product-service na porta 5003..."
	uv run --package product-service python burguer-app/product-service/app.py

test:
	@echo "Rodando testes do auth-service..."
	uv run --package auth-service pytest -v

test-cov:
	@echo "Rodando testes com cobertura..."
	uv run --package auth-service pytest --cov=models --cov=controllers --cov=services --cov=config --cov-report=term-missing

clean:
	@echo "Limpando cache Python..."
	Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force 2>nul || true
	Get-ChildItem -Path . -Include .pytest_cache -Recurse -Directory | Remove-Item -Recurse -Force 2>nul || true
	Get-ChildItem -Path . -Include .coverage -Recurse -File | Remove-Item -Force 2>nul || true
	@echo "Limpando Docker..."
	make docker-clean
	@echo "Feito!"
