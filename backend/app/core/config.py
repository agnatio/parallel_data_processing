"""
Application configuration settings loaded from environment variables
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Settings
    PROJECT_NAME: str = "FastAPI Backend"
    PROJECT_DESCRIPTION: str = "Professional FastAPI backend application"
    VERSION: str = "0.1.0"
    API_PREFIX: str = ""
    DEBUG: bool = True
    
    # Server settings
    HOST: str = "localhost"
    PORT: int = 8000
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]  # Set to specific origins in production
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Environment-specific configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Create global settings object
settings = Settings()