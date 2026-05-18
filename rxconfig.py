import reflex as rx
import os

api_url = os.environ.get("API_URL")

is_hf_space = bool(os.environ.get("SPACE_ID"))

if not api_url and os.getenv("REFLEX_ENV") == "prod":
    # Reflex Cloud handles api_url automatically.
    # Only use a fallback if absolutely necessary for custom backends.
    api_url= "684e7009-7552-45bc-9825-7de69039782e.fly.dev"
if not api_url:
    api_url = "http://localhost:8000"

config = rx.Config(
    app_name="NeuralCompile",
    api_url=api_url,
    cors_allowed_origins=["*"],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)