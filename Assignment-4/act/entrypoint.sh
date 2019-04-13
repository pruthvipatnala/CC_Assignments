#!/bin/sh

# Collect static files
echo "Running with hostname"
echo $HOSTNAME 

touch assign.db

# Apply database migrations
echo "creating the database"
python3 db_creation.py

echo "running the acts.py"
python3 acts.py
