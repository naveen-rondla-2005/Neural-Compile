# Build Stage
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user (Hugging Face runs containers as user 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory to the user's home
WORKDIR $HOME/app

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and ensure correct ownership
COPY --chown=user . .

# Initialize Reflex and Export the frontend
# Generating the build during Docker construction speeds up HF startup and avoids runtime build errors.
RUN reflex init && reflex export --frontend-only --no-zip

# Ensure the database directory is writable (HF specific)
RUN touch reflex.db && chmod 666 reflex.db

# The port will be provided dynamically by the hosting environment via the $PORT variable.
EXPOSE 7860

# Make the prestart script executable
RUN chmod +x prestart.sh

# Start using the prestart script
CMD ["bash", "prestart.sh"]



