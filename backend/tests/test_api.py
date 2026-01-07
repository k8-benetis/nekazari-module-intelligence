"""
Intelligence Module - API Tests

Basic test suite for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_list_plugins(client):
    """Test plugins listing endpoint."""
    response = client.get("/api/intelligence/plugins")
    assert response.status_code == 200
    data = response.json()
    assert "plugins" in data
    assert isinstance(data["plugins"], list)


