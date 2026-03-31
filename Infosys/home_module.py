"""
home_module.py - Landing page, About, and Help pages for Neural Compile.
"""
import reflex as rx
from .components import navbar, footer


def home_page():
    return rx.vstack(
        navbar(active_page="Home"),
        # Hero
        rx.box(
            rx.center(
                rx.vstack(
                    rx.image(src="/logo.png", width="150px", height="auto", margin_bottom="20px"),
                    rx.badge("🧠 Neural Compile", color_scheme="blue", class_name="hero-badge"),
                    rx.heading(
                        "The AI-Powered Compilation Suite",
                        size="9",
                        text_align="center",
                        class_name="hero-heading",
                        background="linear-gradient(135deg, #e6edf3 0%, #6B73FF 50%, #9747FF 100%)",
                        background_clip="text",
                        color="transparent",
                    ),
                    rx.text(
                        "Write, execute, visualize, and optimize code across multiple languages with Groq-accelerated AI analysis.",
                        text_align="center",
                        color="gray",
                        max_width="600px",
                        class_name="hero-subtext",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button("Open Editor", color_scheme="blue", size="3", class_name="shimmer-btn glow-btn"),
                            href="/editor",
                        ),
                        rx.link(
                            rx.button("Visualize Code", variant="outline", size="3", class_name="shimmer-btn"),
                            href="/visualizer",
                        ),
                        rx.link(
                            rx.button("AI Analyzer", color_scheme="violet", size="3", class_name="shimmer-btn"),
                            href="/analyze",
                        ),
                        spacing="4",
                        class_name="hero-buttons",
                    ),
                    spacing="6",
                    align="center",
                    max_width="800px",
                ),
                width="100%",
                min_height="70vh",
            ),
            width="100%",
            class_name="hero-section",
        ),

        # Features
        rx.vstack(
            rx.heading("Everything You Need", size="7", text_align="center"),
            rx.hstack(
                *[
                    rx.vstack(
                        rx.icon(icon, size=32, color=color),
                        rx.text(title, font_weight="700", size="4"),
                        rx.text(desc, color="gray", text_align="center", size="2"),
                        padding="28px",
                        background="rgba(107,115,255,0.05)",
                        border="1px solid rgba(107,115,255,0.15)",
                        border_radius="16px",
                        align="center",
                        class_name="feature-card",
                        spacing="3",
                        flex="1",
                    )
                    for icon, color, title, desc in [
                        ("code", "#6B73FF",    "Neural IDE",        "Monaco-powered editor with multi-language support and IntelliSense."),
                        ("git-branch", "#9747FF","CFG Viewer",      "Interactive Control Flow Graphs rendered in real-time."),
                        ("monitor-play", "#E36209","Neural Tutor",  "Python Tutor-style line-by-line execution with variable state tracking."),
                        ("zap", "#7ee787",     "AI Code Review",    "Groq-accelerated analysis for bugs, performance, and clean code."),
                        ("history", "#0969DA", "Device History",    "Execution logs partitioned by hardware fingerprint - no login required."),
                    ]
                ],
                width="100%", spacing="4", align="start",
            ),
            width="100%",
            padding="40px",
            max_width="1400px",
            margin_x="auto",
            spacing="8",
        ),

        footer(),
        background_color="var(--bg-color)",
        width="100%",
        spacing="0",
    )


def about_page():
    return rx.vstack(
        navbar(active_page="About"),
        rx.container(
            rx.vstack(
                rx.center(
                    rx.vstack(
                        rx.badge("About Neural Compile", color_scheme="blue", size="3"),
                        rx.heading("Neural Compile: An Agentic Framework for Modern Compilers", size="9", text_align="center"),
                        rx.text(
                            "The evolution of software development requires more than just syntax checking. "
                            "Neural Compile bridges the gap between raw code and human intent using AI-driven agentic reasoning.",
                            max_width="800px", text_align="center", font_size="1.2em", color="gray"
                        ),
                        spacing="6", align="center",
                    ),
                    padding_y="60px",
                ),

                rx.divider(),

                # Problem & Solution
                rx.grid(
                    rx.vstack(
                        rx.heading("The Problem", size="6", color="red"),
                        rx.text("Traditional compilers are deterministic and 'intent-blind'. They can tell you where a semicolon is missing, but they can't understand the semantic logic of a complex algorithm or identify subtle architectural flaws that lead to technical debt."),
                        align="start", spacing="3",
                    ),
                    rx.vstack(
                        rx.heading("The Agentic Solution", size="6", color="green"),
                        rx.text("Neural Compile introduces an 'Agentic' layer. Instead of simple rule-based checks, it utilizes AI agents that reason about your code's Abstract Syntax Tree (AST) and Control Flow Graph (CFG) to provide human-like feedback and optimizations."),
                        align="start", spacing="3",
                    ),
                    columns="2", spacing="8", width="100%", padding_y="40px",
                ),

                rx.divider(),

                # How it works
                rx.vstack(
                    rx.heading("How It Works: Neural Networks & NLP", size="7"),
                    rx.text(
                        "At its core, Neural Compile treats code as a specialized form of natural language. "
                        "By using Transformer-based models via Groq's API acceleration, we perform Natural Language Processing (NLP) "
                        "over the code's structural data. This allows the system to 'reason' about variables, loops, and logic "
                        "just like a senior engineer would during a code review.",
                        max_width="900px",
                    ),
                    rx.hstack(
                        rx.badge("NLP Reasoning", color_scheme="orange"),
                        rx.badge("Graph Analysis", color_scheme="blue"),
                        rx.badge("LLM Orchestration", color_scheme="green"),
                        spacing="3",
                    ),
                    align="start", spacing="4", padding_y="40px",
                ),

                rx.divider(),

                # Future Work
                rx.vstack(
                    rx.heading("The Roadmap: Future Work", size="7"),
                    rx.grid(
                        rx.vstack(
                            rx.heading("Multi-Language Expansion", size="4"),
                            rx.text("Adding deep support for low-level systems languages like C++ and Rust, including memory safety analysis."),
                            align="start",
                        ),
                        rx.vstack(
                            rx.heading("Real-time Agentic Fixes", size="4"),
                            rx.text("Moving beyond analysis to 'Self-Healing' code where agents suggest and apply fixes as you type."),
                            align="start",
                        ),
                        rx.vstack(
                            rx.heading("Git & CI/CD Integration", size="4"),
                            rx.text("Automated agentic code reviews integrated directly into your Pull Request workflow."),
                            align="start",
                        ),
                        rx.vstack(
                            rx.heading("Deep AST Reasoning", size="4"),
                            rx.text("Enhanced mapping between visual AST nodes and semantic intent for even more precise bug detection."),
                            align="start",
                        ),
                        columns="2", spacing="6", width="100%",
                    ),
                    align="start", spacing="6", padding_y="40px",
                ),

                spacing="8",
                width="100%",
                padding_x="20px",
            ),
            max_width="1000px",
            margin_x="auto",
        ),
        footer(),
        background_color="var(--bg-color)", width="100%",
        padding_bottom="100px",
    )


def help_page():
    return rx.vstack(
        navbar(active_page="Help"),
        rx.center(
            rx.vstack(
                rx.badge("Help & Documentation", color_scheme="green"),
                rx.heading("Getting Started", size="8"),
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.badge(step, color_scheme="blue", variant="soft"),
                            rx.text(desc, size="3"),
                            spacing="4", align="center",
                        )
                        for step, desc in [
                            ("1", "Navigate to /editor or /visualizer"),
                            ("2", "Select your programming language from the dropdown"),
                            ("3", "Write or paste your code in the Monaco editor"),
                            ("4", "Click RUN to execute, VISUALIZE to trace line-by-line, or AI FIX to review"),
                            ("5", "Your sessions are automatically saved and viewable at /history"),
                        ]
                    ],
                    spacing="4", align="start",
                ),
                spacing="6", align="start", max_width="600px",
            ),
            min_height="70vh", width="100%",
        ),
        footer(),
        background_color="var(--bg-color)", width="100%",
    )
