"""
Tests for the root endpoint
"""
from fastapi import status
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """
    Test that the root endpoint returns a welcome message.
    
    Args:
        client: The test client fixture
    """
    # When
    response = client.get("/")
    
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert "API is running" in response.json()["message"]
    assert "docs" in response.json()["message"]