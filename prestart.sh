#!/bin/bash
# Robust prestart script for Reflex on Hugging Face Spaces
# This script handles database initialization and migration before launching the app.

LOGFILE="/home/user/app/startup.log"
echo "$(date): Starting prestart sequence..." > "$LOGFILE"

# Ensure we're in the right directory
cd /home/user/app || cd .
echo "$(date): Working directory: $(pwd)" >> "$LOGFILE"

# Force database initialization
echo "$(date): Attempting database initialization..." >> "$LOGFILE"
# 'reflex db init' creates the alembic environment (if missing) and local sqlite db.
# We ignore errors if it's already initialized.
reflex db init >> "$LOGFILE" 2>&1

# Apply migrations
echo "$(date): Applying database migrations..." >> "$LOGFILE"
reflex db migrate >> "$LOGFILE" 2>&1

# Double check if the database file exists
if [ -f "reflex.db" ]; then
    echo "$(date): Database file (reflex.db) verified." >> "$LOGFILE"
else
    echo "$(date): WARNING: reflex.db not found after initialization!" >> "$LOGFILE"
fi

# Launch the application on port 7860 (Hugging Face requirement)
echo "$(date): Launching Neural Compile on port 7860..." >> "$LOGFILE"
# We bind both frontend and backend to 7860 for single-port environments.
exec reflex run --env prod --backend-port 7860 --frontend-port 7860
