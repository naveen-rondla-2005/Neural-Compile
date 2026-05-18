"""
NeuralCompile — /health endpoint
Used by Docker HEALTHCHECK and monitoring systems.
Returns JSON: {"status": "ok", "service": "NeuralCompile", "uptime_seconds": <float>}
"""

import time
import reflex as rx

_START_TIME = time.time()


def health_page() -> rx.Component:
    """Lightweight health check page rendered as JSON-like text."""
    uptime = round(time.time() - _START_TIME, 2)
    payload = (
        "{"
        f'"status": "ok", '
        f'"service": "NeuralCompile", '
        f'"uptime_seconds": {uptime}'
        "}"
    )
    return rx.el.pre(
        payload,
        style={
            "fontFamily": "monospace",
            "padding": "1rem",
            "color": "#22c55e",
            "background": "#0f172a",
            "minHeight": "100vh",
            "margin": "0",
        },
    )
