"""
Global exception handlers for the API
"""
import logging
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


logger = logging.getLogger("app")


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled exceptions.
    
    Args:
        request: The FastAPI request object
        exc: The exception that was raised
        
    Returns:
        A JSON response with an error message
    """
    # Log the exception with traceback
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Exception handler for request validation errors.
    
    Args:
        request: The FastAPI request object
        exc: The validation exception that was raised
        
    Returns:
        A JSON response with validation error details
    """
    logger.warning(f"Validation error: {exc}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Register all exception handlers with the FastAPI application.
    
    Args:
        app: The FastAPI application instance
    """
    # Register handlers for specific exception types
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    # Register handler for all unhandled exceptions
    app.add_exception_handler(Exception, generic_exception_handler)