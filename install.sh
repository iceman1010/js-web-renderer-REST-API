#!/bin/bash
set -e

# js-web-renderer REST API Installation Script
# Run this on the target server (whisper1)

INSTALL_DIR="/opt/js-web-renderer-api"
SERVICE_NAME="js-web-renderer-api"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing js-web-renderer REST API..."

# Create install directory
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p /opt/js-web-renderer/profiles

# Copy files
sudo cp -r "$SCRIPT_DIR/app" "$INSTALL_DIR/"
sudo cp "$SCRIPT_DIR/requirements.txt" "$INSTALL_DIR/"
sudo cp "$SCRIPT_DIR/.env.example" "$INSTALL_DIR/"

# Create .env if it doesn't exist
if [ ! -f "$INSTALL_DIR/.env" ]; then
    API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    sudo cp "$INSTALL_DIR/.env.example" "$INSTALL_DIR/.env"
    sudo sed -i "s/your-secret-api-key-here/$API_KEY/" "$INSTALL_DIR/.env"
    echo "Generated API key: $API_KEY"
    echo "Save this key - it's stored in $INSTALL_DIR/.env"
fi

# Install Python dependencies
cd "$INSTALL_DIR"
sudo pip3 install -r requirements.txt

# Install systemd service
sudo cp "$SCRIPT_DIR/js-web-renderer-api.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo ""
echo "Installation complete!"
echo "Service status: systemctl status $SERVICE_NAME"
echo "View logs: journalctl -u $SERVICE_NAME -f"
echo "API docs: http://$(hostname):9000/docs"
