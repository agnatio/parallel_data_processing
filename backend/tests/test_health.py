"""
Tests for the health endpoint
"""
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


def test_health_endpoint(client: TestClient) -> None:
    """
    Test that the health endpoint returns the expected status and data.
    
    Args:
        client: The test client fixture
    """
    # When
    response = client.get("/health")
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    
    response_data = response.json()
    assert response_data["status"] == "healthy"
    assert response_data["version"] == settings.VERSION
    assert response_data["service"] == "fastapi-backend"


def test_health_endpoint_not_authenticated(client: TestClient) -> None:
    """
    Test that the health endpoint doesn't require authentication.
    
    Args:
        client: The test client fixture
    """
    # When: Accessing health endpoint without authentication
    response = client.get("/health")
    
    # Then: Should succeed without auth
    assert response.status_code == status.HTTP_200_OK