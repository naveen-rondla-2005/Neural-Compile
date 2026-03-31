import reflex as rx
import os

# Prioritize API_URL from environment variables (useful for Render/Docker)
api_url = os.environ.get("API_URL")

# Fallback: Determine if we are running in a Hugging Face Space
if not api_url:
    is_hf = os.environ.get("HUGGINGFACE_SPACES") or os.environ.get("SPACE_ID")
    if is_hf:
        space_id = os.environ.get("SPACE_ID", "")
        if "/" in space_id:
            user, space = space_id.split("/")
            api_url = f"https://neuralcompile-neon-sun.reflex.run"
        else:
            api_url = "https://neuralcompile-neon-sun.reflex.run"
    else:
        api_url = "https://neuralcompile-neon-sun.reflex.run"

config = rx.Config(
    app_name="Infosys",
    api_url=api_url,
    cors_allowed_origins=["*"],
    prerender=False, # Disable prerendering to fix SSR 'invalid element' errors
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)