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
    # 2. Local/Cloud: Let Reflex handle it via environment or default to localhost
    else:
        api_url = os.environ.get("API_URL", "http://localhost:8000")

config = rx.Config(
    app_name="Infosys",
    api_url=api_url,
    cors_allowed_origins=["*"],
    prerender=True, 
    plugins=[
        rx.plugins.SitemapPlugin(),
        # rx.plugins.TailwindV4Plugin(), # Disabled to isolate potential build issues
    ]
)