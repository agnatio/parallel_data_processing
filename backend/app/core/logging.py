"""
Logging configuration for the application
"""
import logging
import sys
from typing import Optional


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Configure and return the root logger for the application
    
    Args:
        log_level: Optional override for the log level
        
    Returns:
        The configured logger instance
    """
    # Set default log level if not provided
    if log_level is None:
        log_level = "INFO"
    
    # Configure the root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    
    # Get and return the logger for the app
    logger = logging.getLogger("app")
    
    # Disable propagation to avoid duplicate logs
    logger.propagate = False
    
    return logger