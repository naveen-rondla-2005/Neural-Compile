# =============================================================================
# NeuralCompile — Makefile
# =============================================================================
# Quick reference:
#   make help          → show all available commands
#   make install       → install Python dependencies
#   make run           → run in normal (local) mode
#   make docker-dev    → run in Docker dev mode (hot-reload)
#   make docker-prod   → run in Docker prod mode (single port)
#   make docker-nginx  → run Docker prod + Nginx reverse proxy
#   make docker-build  → build Docker images
#   make docker-down   → stop all containers
#   make docker-logs   → follow container logs
#   make lint          → run ruff linter
#   make clean         → remove build artefacts
# =============================================================================

.PHONY: help install run \
        docker-dev docker-prod docker-nginx \
        docker-build docker-down docker-logs \
        lint clean

# Colours for pretty output
GREEN  := \033[0;32m
YELLOW := \033[1;33m
CYAN   := \033[0;36m
RESET  := \033[0m

## ── Help ───────────────────────────────────────────────────────────────────

help:
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════════╗$(RESET)"
	@echo "$(CYAN)║        NeuralCompile — Developer Commands        ║$(RESET)"
	@echo "$(CYAN)╚══════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(YELLOW)── Local Mode ──────────────────────────────────────$(RESET)"
	@echo "  $(GREEN)make install$(RESET)       Install Python dependencies"
	@echo "  $(GREEN)make run$(RESET)           Start app locally (reflex run)"
	@echo ""
	@echo "$(YELLOW)── Docker Mode ─────────────────────────────────────$(RESET)"
	@echo "  $(GREEN)make docker-build$(RESET)  Build Docker image(s)"
	@echo "  $(GREEN)make docker-dev$(RESET)    Start app in Docker dev mode (hot-reload)"
	@echo "  $(GREEN)make docker-prod$(RESET)   Start app in Docker prod mode"
	@echo "  $(GREEN)make docker-nginx$(RESET)  Start prod + Nginx reverse proxy"
	@echo "  $(GREEN)make docker-down$(RESET)   Stop and remove containers"
	@echo "  $(GREEN)make docker-logs$(RESET)   Follow container logs"
	@echo ""
	@echo "$(YELLOW)── Code Quality ────────────────────────────────────$(RESET)"
	@echo "  $(GREEN)make lint$(RESET)          Run ruff linter"
	@echo "  $(GREEN)make clean$(RESET)         Remove build artefacts"
	@echo ""

## ── Local Mode ─────────────────────────────────────────────────────────────

install:
	@echo "$(CYAN)▶ Installing Python dependencies...$(RESET)"
	@pip install -r requirements.txt
	@echo "$(GREEN)✔ Done.$(RESET)"

run:
	@echo "$(CYAN)▶ Starting NeuralCompile in local mode...$(RESET)"
	@echo "$(YELLOW)  URL: http://localhost:3000$(RESET)"
	@reflex run

## ── Docker Mode ─────────────────────────────────────────────────────────────

docker-build:
	@echo "$(CYAN)▶ Building Docker images...$(RESET)"
	@docker compose build
	@echo "$(GREEN)✔ Build complete.$(RESET)"

docker-dev:
	@echo "$(CYAN)▶ Starting NeuralCompile in Docker DEV mode...$(RESET)"
	@echo "$(YELLOW)  Frontend: http://localhost:3000$(RESET)"
	@echo "$(YELLOW)  Backend:  http://localhost:8000$(RESET)"
	@docker compose --profile dev up

docker-prod:
	@echo "$(CYAN)▶ Starting NeuralCompile in Docker PROD mode...$(RESET)"
	@echo "$(YELLOW)  URL: http://localhost:3000$(RESET)"
	@docker compose --profile prod up -d
	@echo "$(GREEN)✔ Container started. Run 'make docker-logs' to follow logs.$(RESET)"

docker-nginx:
	@echo "$(CYAN)▶ Starting NeuralCompile with Nginx reverse proxy...$(RESET)"
	@echo "$(YELLOW)  URL: http://localhost:80$(RESET)"
	@docker compose --profile prod --profile nginx up -d
	@echo "$(GREEN)✔ Started. Nginx → app on port 80.$(RESET)"

docker-down:
	@echo "$(CYAN)▶ Stopping all containers...$(RESET)"
	@docker compose --profile dev --profile prod --profile nginx down
	@echo "$(GREEN)✔ All containers stopped.$(RESET)"

docker-logs:
	@docker compose --profile dev --profile prod logs -f

## ── Code Quality ─────────────────────────────────────────────────────────────

lint:
	@echo "$(CYAN)▶ Running ruff linter...$(RESET)"
	@ruff check NeuralCompile/ || true
	@echo "$(GREEN)✔ Lint complete.$(RESET)"

## ── Cleanup ──────────────────────────────────────────────────────────────────

clean:
	@echo "$(CYAN)▶ Cleaning build artefacts...$(RESET)"
	@rm -rf .web/dist __pycache__ NeuralCompile/__pycache__
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@echo "$(GREEN)✔ Clean complete.$(RESET)"
