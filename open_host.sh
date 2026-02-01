#!/bin/bash
# Script to open the host.html file in the default browser

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOST_FILE="$SCRIPT_DIR/frontend/host.html"

# Open in default browser (works on macOS and Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$HOST_FILE"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$HOST_FILE"
else
    echo "Please open $HOST_FILE manually in your browser"
fi
