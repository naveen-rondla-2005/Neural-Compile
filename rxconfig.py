import reflex as rx
import os

# Prioritize API_URL from environment variables (useful for Render/Docker)
api_url = os.environ.get("API_URL")

# Fallback logic for different environments
if not api_url:
    # 1. Check for Hugging Face Spaces
    space_id = os.environ.get("SPACE_ID")
    if space_id:
        user, space = space_id.split("/")
        api_url = f"https://{user}-{space.replace('.', '-')}.hf.space"
    # 2. Check if we are running on Reflex Cloud (using their generic subdomain)
    elif os.environ.get("REFLEX_CLOUD") == "true":
        api_url = "https://neuralcompile-neon-sun.reflex.run"
    # 3. Default to Local Development
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