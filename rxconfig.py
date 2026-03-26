import reflex as rx
import os

# Determine if we are running in a Hugging Face Space
is_hf = os.environ.get("HUGGINGFACE_SPACES") or os.environ.get("SPACE_ID")
# For HF Spaces, the URL is typically https://{user}-{space-name}.hf.space
# We can infer it from SPACE_ID which is "user/space-name"
if is_hf:
    space_id = os.environ.get("SPACE_ID", "")
    if "/" in space_id:
        user, space = space_id.split("/")
        api_url = f"https://{user}-{space.replace('.', '-')}.hf.space"
    else:
        api_url = ""
else:
    api_url = "http://localhost:8000"

config = rx.Config(
    app_name="Infosys",
    api_url=api_url,
    cors_allowed_origins=["*"],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)