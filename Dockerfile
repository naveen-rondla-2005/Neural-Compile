# Build Stage
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    unzip \
    && rm -rf /var/lib/apt/node_modules

# Create a non-root user (Hugging Face runs containers as user 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory to the user's home
WORKDIR $HOME/app

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and ensure correct ownership
COPY --chown=user . .

# Initialize Reflex (creates .web directory)
RUN reflex init

# Expose the port used by Hugging Face Spaces
EXPOSE 7860

# Ensure Reflex knows which port to bind to
ENV PORT=7860
ENV HOST=0.0.0.0

# Make the prestart script executable
RUN chmod +x prestart.sh

# Start using the prestart script which handles DB initialization
CMD ["bash", "prestart.sh"]



