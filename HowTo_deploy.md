# How to Deploy and Test

## Deployment

### Quick Deploy

```bash
./deploy.sh
```

This will:
1. Pull latest code from GitHub on whisper1 server
2. Fix permissions (ensure CLI is executable)
3. Restart the js-web-renderer-api service

### Manual Deploy

```bash
# On the server
cd /opt/js-web-renderer-api
git fetch origin master
git reset --hard origin/master

# Restart service
sudo systemctl restart js-web-renderer-api
```

## Testing

### Prerequisites

```bash
pip3 install pytest pytest-asyncio httpx
```

### Environment Variables

Get the API key from the server:
```bash
ssh whisper1 "cat /opt/js-web-renderer-api/.env | grep API_KEY"
```

Set environment variables:
```bash
export API_KEY="your-api-key-from-above"
export TEST_BASE_URL="http://whisper1:9000"
```

### Run Tests

```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/test_api.py        # REST API tests
pytest tests/test_cli.py        # CLI tool tests (via SSH)
pytest tests/test_concurrency.py # Concurrency limiting tests

# Run specific test
pytest tests/test_api.py::TestAPI::test_render_with_auth

# Run multiple specific tests
pytest tests/test_api.py::TestAPI::test_render_with_auth tests/test_api.py::TestAPI::test_network_with_auth
```

## Health Check

```bash
curl http://whisper1:9000/health
```

Response:
```json
{
  "status": "healthy",
  "renderer_available": true,
  "active_instances": 0,
  "max_instances": 4
}
```

## Troubleshooting

### Service not responding

```bash
# Check service status
ssh whisper1 "sudo systemctl status js-web-renderer-api"

# Check logs
ssh whisper1 "sudo journalctl -u js-web-renderer-api -n 50 --no-pager"

# Restart service
ssh whisper1 "sudo systemctl restart js-web-renderer-api"
```

### Tests timing out

Increase the timeout in test calls:
```python
httpx.post(url, json=data, headers=HEADERS, timeout=60)
```
