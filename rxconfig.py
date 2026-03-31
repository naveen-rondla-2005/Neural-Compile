import reflex as rx
import os

# Prioritize API_URL from environment variables (useful for Render/Docker)
api_url = os.environ.get("API_URL")

# Fallback logic for different environments
if not api_url:
    # 1. Hugging Face Spaces detection
    space_id = os.environ.get("SPACE_ID")
    if space_id:
        user, space = space_id.split("/")
        api_url = f"https://{user}-{space.replace('.', '-')}.hf.space"
    # 2. Reflex Cloud detection (using their system variables)
    elif os.environ.get("REFLEX_APP_URL"):
        api_url = os.environ.get("REFLEX_APP_URL")
    # 3. Last resort fallback for production (if we aren't local but URL unknown)
    elif os.environ.get("ENV") == "prod":
        api_url = "" # Let Reflex infer the URL from the current origin
    # 4. Local Development
    else:
        api_url = "http://localhost:8000"

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