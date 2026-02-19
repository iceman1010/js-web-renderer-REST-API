#!/bin/bash
set -e

echo "Deploying to whisper1..."
ssh whisper1 "cd /opt/js-web-renderer-api && git fetch origin master && git reset --hard origin/master"

# Fix permissions - js-web-render user needs to read the CLI
ssh whisper1 "sudo chmod +x /opt/js-web-renderer/bin/fetch-rendered.py"

ssh whisper1 "sudo systemctl restart js-web-renderer-api && sudo systemctl status js-web-renderer-api --no-pager"

echo "Deployment complete!"
