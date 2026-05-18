# syntax=docker/dockerfile:1
# =============================================================================
# NeuralCompile — Multi-Stage Dockerfile
# =============================================================================
# Stages:
#   base  → shared OS + system deps
#   deps  → Python dependency layer (cached separately for fast rebuilds)
#   dev   → local development with hot-reload  (docker compose --profile dev)
#   prod  → optimised production image         (default / HF Spaces)
# =============================================================================

# ─── Stage 1: base ───────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

LABEL maintainer="Naveen Rondla <naveenrondla@hotmail.com>"
LABEL org.opencontainers.image.title="NeuralCompile"
LABEL org.opencontainers.image.description="AI-Powered IDE & Code Visualizer"
LABEL org.opencontainers.image.source="https://github.com/naveen-rondla-2005/Neural-Compile"

# Install only the OS packages we truly need.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl \
    graphviz \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user (Hugging Face Spaces requires uid 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# ─── Stage 2: deps ───────────────────────────────────────────────────────────
# This layer is rebuilt ONLY when requirements.txt changes — maximising cache hits.
FROM base AS deps

COPY --chown=user requirements.txt .
RUN --mount=type=cache,target=/home/user/.cache/pip,uid=1000 \
    pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ─── Stage 3: dev ────────────────────────────────────────────────────────────
# Local development target — mounts source via docker compose volume,
# so code changes are reflected instantly without rebuilding.
FROM deps AS dev

ENV REFLEX_ENV=dev
EXPOSE 3000 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

CMD ["reflex", "run", "--env", "dev"]

# ─── Stage 4: prod ───────────────────────────────────────────────────────────
# Production target — copies source into the image, builds frontend, and runs
# in single-port mode. Compatible with Hugging Face Spaces (port 7860, uid 1000).
FROM deps AS prod

# Copy application source
COPY --chown=user . .

# Initialise Reflex (scaffolds .web directory). Frontend build is deferred to
# prestart.sh so this heavy step does NOT run on every Docker build.
RUN reflex init

# Ensure the SQLite file is writable
RUN touch reflex.db && chmod 666 reflex.db

# Make startup script executable
RUN chmod +x prestart.sh

ENV REFLEX_ENV=prod
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD curl -f http://localhost:${PORT:-7860}/health || exit 1

CMD ["bash", "prestart.sh"]
