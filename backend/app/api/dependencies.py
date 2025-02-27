"""
Reusable dependencies for FastAPI route handlers
"""
import logging
from typing import Annotated

from fastapi import Depends, Request, Path

from app.core.config import settings


logger = logging.getLogger("app")


async def get_api_version() -> str:
    """
    Dependency that returns the API version.
    
    Returns:
        The current API version string
    """
    return settings.VERSION


async def request_audit_log(request: Request) -> None:
    """
    Dependency for request auditing.
    
    Args:
        request: The FastAPI request object
    """
    logger.info(f"Request received: {request.method} {request.url.path}")


# Alias types for common dependencies
APIVersion = Annotated[str, Depends(get_api_version)]
AuditLog = Annotated[None, Depends(request_audit_log)]