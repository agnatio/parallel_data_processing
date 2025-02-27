"""
Pytest configuration and fixtures
"""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app as fastapi_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """
    Get the FastAPI application instance.
    
    Returns:
        The FastAPI application for testing
    """
    return fastapi_app


@pytest.fixture(scope="module")
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    """
    Create a FastAPI TestClient for testing API endpoints.
    
    Args:
        app: The FastAPI application instance
        
    Returns:
        A TestClient instance for making requests
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an event loop for async tests.
    
    Returns:
        An event loop instance
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()