"""
Health check endpoints
"""
from typing import Dict, Any

from fastapi import APIRouter, status

from app.api.dependencies import APIVersion, AuditLog


# Create router for health endpoints
router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get(
    "",  # Empty prefix as it's added to the router
    summary="Health Check",
    response_description="Health status of the application",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        JSON response with status and version information.
    """
    from app.core.config import settings
    
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": "fastapi-backend"
    }