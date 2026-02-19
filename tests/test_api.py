import pytest
import httpx
import os


# Get API key from environment or use test key
API_KEY = os.environ.get("API_KEY", "test-api-key")
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:9000")
HEADERS = {"X-API-Key": API_KEY}


class TestAPI:
    """Test the REST API endpoints."""

    def test_health_no_auth(self):
        """Test health endpoint without authentication."""
        response = httpx.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "renderer_available" in data
        assert "active_instances" in data
        assert "max_instances" in data

    def test_health_shows_instances(self):
        """Test health endpoint shows instance counts."""
        response = httpx.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["active_instances"], int)
        assert isinstance(data["max_instances"], int)
        assert data["max_instances"] == 4  # Default MAX_INSTANCES

    def test_render_requires_auth(self):
        """Test render endpoint requires authentication."""
        response = httpx.post(
            f"{BASE_URL}/render",
            json={"url": "https://example.com", "wait": 2}
        )
        # Without auth header, should get 401 or 403
        assert response.status_code in [401, 403]

    def test_render_with_auth(self):
        """Test render endpoint with authentication."""
        response = httpx.post(
            f"{BASE_URL}/render",
            json={"url": "https://example.com", "wait": 3},
            headers=HEADERS,
            timeout=60
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["html"] is not None
        assert len(data["html"]) > 0

    def test_screenshot_with_auth(self):
        """Test screenshot endpoint with authentication."""
        response = httpx.post(
            f"{BASE_URL}/screenshot",
            json={"url": "https://example.com", "wait": 3, "width": 800, "height": 600},
            headers=HEADERS,
            timeout=60
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert len(response.content) > 0

    def test_network_with_auth(self):
        """Test network capture endpoint with authentication."""
        response = httpx.post(
            f"{BASE_URL}/network",
            json={"url": "https://example.com", "wait": 3},
            headers=HEADERS,
            timeout=60
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "requests" in data

    def test_profiles_list_requires_auth(self):
        """Test profiles list requires authentication."""
        response = httpx.get(f"{BASE_URL}/profiles")
        assert response.status_code in [401, 403]

    def test_profiles_list_with_auth(self):
        """Test profiles list with authentication."""
        response = httpx.get(f"{BASE_URL}/profiles", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert "profiles" in data
        assert isinstance(data["profiles"], list)

    def test_profiles_create_and_delete(self):
        """Test profile creation and deletion."""
        import uuid
        profile_name = f"test-profile-{uuid.uuid4().hex[:8]}"
        
        # Create profile
        response = httpx.post(
            f"{BASE_URL}/profiles",
            json={"name": profile_name},
            headers=HEADERS
        )
        assert response.status_code == 200
        
        # Get profile info
        response = httpx.get(f"{BASE_URL}/profiles/{profile_name}", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["exists"] is True
        
        # Delete profile
        response = httpx.delete(f"{BASE_URL}/profiles/{profile_name}", headers=HEADERS)
        assert response.status_code == 200
        
        # Verify deleted
        response = httpx.get(f"{BASE_URL}/profiles/{profile_name}", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["exists"] is False

    def test_profiles_duplicate_fails(self):
        """Test creating duplicate profile fails."""
        import uuid
        profile_name = f"test-profile-dup-{uuid.uuid4().hex[:8]}"
        
        # Create profile
        httpx.post(
            f"{BASE_URL}/profiles",
            json={"name": profile_name},
            headers=HEADERS
        )
        
        # Try to create again
        response = httpx.post(
            f"{BASE_URL}/profiles",
            json={"name": profile_name},
            headers=HEADERS
        )
        assert response.status_code == 409
        
        # Cleanup
        httpx.delete(f"{BASE_URL}/profiles/{profile_name}", headers=HEADERS)

    def test_invalid_url(self):
        """Test render with invalid URL."""
        response = httpx.post(
            f"{BASE_URL}/render",
            json={"url": "not-a-valid-url", "wait": 1},
            headers=HEADERS
        )
        # Should either succeed with error in response or fail
        assert response.status_code in [200, 400, 500]

    def test_render_response_structure(self):
        """Test render response has correct structure."""
        response = httpx.post(
            f"{BASE_URL}/render",
            json={"url": "https://example.com", "wait": 3},
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "html" in data
        assert "current_url" in data
