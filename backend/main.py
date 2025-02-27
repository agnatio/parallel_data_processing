"""
FastAPI Backend Application Entry Point
"""
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.events import lifespan
from app.api.dependencies import get_api_version
from app.api.routes.health import router as health_router
from app.api.routes.csv_files import router as csv_files_router  # Import the new CSV files router
from app.api.error_handlers import setup_exception_handlers


# Configure logging
logger = setup_logging()


# Create FastAPI application with lifespan manager
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# Root endpoint with redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root path to API documentation."""
    return {"message": "API is running. Visit /docs for documentation."}


# Register routers
app.include_router(health_router)
app.include_router(csv_files_router)  # Register the CSV files router


# Setup exception handlers
setup_exception_handlers(app)


# Run the application using Uvicorn when executed directly
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )