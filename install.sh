#!/bin/bash
# Install script for code-collect

set -e

echo "Installing code-collect..."

# Check if fzf is installed
if ! command -v fzf &> /dev/null; then
    echo "Error: fzf is required but not installed."
    echo "Install with: brew install fzf (macOS) or apt install fzf (Ubuntu)"
    exit 1
fi

# Make script executable
chmod +x code-collect

# Install globally
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sudo cp code-collect /usr/local/bin/
    echo "✅ Installed to /usr/local/bin/code-collect"
else
    # Linux
    sudo cp code-collect /usr/local/bin/
    echo "✅ Installed to /usr/local/bin/code-collect"
fi

echo "🎉 Installation complete! Run 'code-collect' from any directory."
