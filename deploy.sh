#!/bin/bash
set -e

echo "Deploying to whisper1..."
ssh whisper1 "cd /opt/js-web-renderer-api && git fetch origin master && git reset --hard origin/master"
ssh whisper1 "sudo systemctl restart js-web-renderer-api && sudo systemctl status js-web-renderer-api --no-pager"

echo "Deployment complete!"
