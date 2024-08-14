#!/bin/bash

echo "Pulling latest changes from Git..."
git pull

echo "Restarting the Discord bot..."
pkill -f main.py  # Replace bot_script.py with your bot's main script name
python3 main.py & # Replace bot_script.py with your bot's main script name
