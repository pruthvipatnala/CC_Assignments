#!/bin/sh

# Collect static files
echo "Running with hostname"
echo $HOSTNAME 

# Apply database migrations
echo "creating the database"
python3 db_creation.py

echo "running the acts.py"
python3 user.py