"""
Application lifecycle event handlers for startup and shutdown
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI


logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Handles startup and shutdown events.
    
    Args:
        app: The FastAPI application instance
    """
    # Startup: Initialize resources
    logger.info("Starting up application...")
    
    # Here you would initialize resources like:
    # - Database connections
    # - Background tasks
    # - Cache systems
    # - External API clients
    
    yield  # Application runs here
    
    # Shutdown: Clean up resources
    logger.info("Shutting down application...")
    
    # Here you would clean up resources like:
    # - Closing database connections
    # - Stopping background tasks
    # - Clearing caches