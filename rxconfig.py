import reflex as rx
import os

# Determine the api_url based on the deployment environment.
# - Hugging Face Spaces (single-port mode): Do NOT set api_url; browser uses same origin.
# - Reflex Cloud: Set explicitly via API_URL env var.
# - Local dev: Leave as None (defaults to localhost).

api_url = os.environ.get("API_URL")  # Explicit override always wins

# For Hugging Face Spaces with --single-port, api_url MUST be None.
# The SPACE_ID env var is set automatically by HF; we use it to detect that environment.
is_hf_space = bool(os.environ.get("SPACE_ID"))

# Reflex Cloud production fallback
if not api_url and not is_hf_space and os.getenv("REFLEX_ENV") == "prod":
    api_url = "https://neuralcompile-lime-sun.reflex.run"

config = rx.Config(
    app_name="NeuralCompile",
    api_url=api_url if api_url and not is_hf_space else None,
    cors_allowed_origins=["*"],
    plugins=[
        rx.plugins.SitemapPlugin(),
    ],
)