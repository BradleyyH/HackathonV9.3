#!/bin/bash
# Script to open the fruit_player.html file in the default browser

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FRUIT_FILE="$SCRIPT_DIR/frontend/fruit_player.html"

# Open in default browser (works on macOS and Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$FRUIT_FILE"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$FRUIT_FILE"
else
    echo "Please open $FRUIT_FILE manually in your browser"
fi
