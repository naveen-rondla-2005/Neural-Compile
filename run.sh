#!/bin/bash
# =============================================================================
# NeuralCompile — Universal Launcher
# =============================================================================
# Usage:
#   ./run.sh              → Start in normal local mode (reflex run)
#   ./run.sh --docker     → Start in Docker dev mode   (docker compose)
#   ./run.sh --docker-prod→ Start in Docker prod mode
#   ./run.sh --help       → Show this help message
# =============================================================================

set -e

# ── Colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ── Banner ────────────────────────────────────────────────────────────────────
print_banner() {
    echo ""
    echo -e "${CYAN}${BOLD}╔═══════════════════════════════════════════╗${RESET}"
    echo -e "${CYAN}${BOLD}║       🧠  NeuralCompile Launcher  🧠      ║${RESET}"
    echo -e "${CYAN}${BOLD}║      AI-Powered IDE & Code Visualizer     ║${RESET}"
    echo -e "${CYAN}${BOLD}╚═══════════════════════════════════════════╝${RESET}"
    echo ""
}

# ── Help ──────────────────────────────────────────────────────────────────────
print_help() {
    echo -e "${BOLD}Usage:${RESET}"
    echo -e "  ${GREEN}./run.sh${RESET}               Start locally (normal mode)"
    echo -e "  ${GREEN}./run.sh --docker${RESET}      Start in Docker dev mode"
    echo -e "  ${GREEN}./run.sh --docker-prod${RESET} Start in Docker prod mode"
    echo -e "  ${GREEN}./run.sh --help${RESET}        Show this message"
    echo ""
}

# ── Pre-flight checks ─────────────────────────────────────────────────────────
check_env() {
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠  No .env file found.${RESET}"
        if [ -f ".env.example" ]; then
            echo -e "   Copying .env.example → .env ..."
            cp .env.example .env
            echo -e "${RED}   ✏  Please edit .env and set your GROQ_API_KEY before continuing.${RESET}"
            exit 1
        else
            echo -e "${RED}   ✗  No .env.example found either. Please create a .env file.${RESET}"
            exit 1
        fi
    fi
}

check_python_deps() {
    if ! python3 -c "import reflex" &>/dev/null; then
        echo -e "${YELLOW}⚠  Reflex not found. Installing dependencies...${RESET}"
        pip install -r requirements.txt
    fi
}

check_docker() {
    if ! command -v docker &>/dev/null; then
        echo -e "${RED}✗  Docker is not installed. Please install Docker Desktop.${RESET}"
        echo -e "   → https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    if ! docker info &>/dev/null; then
        echo -e "${RED}✗  Docker daemon is not running. Please start Docker Desktop.${RESET}"
        exit 1
    fi
}

# ── Modes ─────────────────────────────────────────────────────────────────────
run_local() {
    echo -e "${CYAN}▶  Mode: ${BOLD}Local (normal)${RESET}"
    check_env
    check_python_deps
    echo -e "${GREEN}✔  Starting NeuralCompile...${RESET}"
    echo -e "${YELLOW}   URL: http://localhost:3000${RESET}"
    echo ""
    reflex run
}

run_docker_dev() {
    echo -e "${CYAN}▶  Mode: ${BOLD}Docker (dev — hot-reload)${RESET}"
    check_env
    check_docker
    echo -e "${GREEN}✔  Building & starting containers...${RESET}"
    echo -e "${YELLOW}   Frontend: http://localhost:3000${RESET}"
    echo -e "${YELLOW}   Backend:  http://localhost:8000${RESET}"
    echo ""
    docker compose --profile dev up --build
}

run_docker_prod() {
    echo -e "${CYAN}▶  Mode: ${BOLD}Docker (prod — single port)${RESET}"
    check_env
    check_docker
    echo -e "${GREEN}✔  Building & starting containers...${RESET}"
    echo -e "${YELLOW}   URL: http://localhost:3000${RESET}"
    echo ""
    docker compose --profile prod up --build -d
    echo ""
    echo -e "${GREEN}✔  Container is running in the background.${RESET}"
    echo -e "   Run ${CYAN}docker compose --profile prod logs -f${RESET} to follow logs."
}

# ── Entry Point ───────────────────────────────────────────────────────────────
print_banner

case "${1:-}" in
    --help|-h)
        print_help
        ;;
    --docker)
        run_docker_dev
        ;;
    --docker-prod)
        run_docker_prod
        ;;
    "")
        run_local
        ;;
    *)
        echo -e "${RED}✗  Unknown option: $1${RESET}"
        print_help
        exit 1
        ;;
esac
