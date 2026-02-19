"""Configuration"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    APP_NAME: str = "ChurnLogic"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/churnlogic"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # ML
    MODEL_PATH: str = "./models/"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024
    TEST_SIZE: float = 0.2
    RANDOM_STATE: int = 42
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()