"""Configuration settings for EarningsCall-TLDR"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    
    # Data directories
    DATA_DIR: Path = Path("../data")
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    CACHE_DIR: Path = DATA_DIR / "cache"
    REPORTS_DIR: Path = DATA_DIR / "reports"
    
    # Database
    DATABASE_URL: str = "sqlite:///../data/earnings.db"
    
    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.1
    MAX_TOKENS: int = 2000
    
    # RAG settings
    MAX_CHUNK_SIZE: int = 1200
    MIN_CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    TOP_K_RETRIEVAL: int = 5
    
    # Data providers
    YAHOO_FINANCE_ENABLED: bool = True
    ALPHA_VANTAGE_ENABLED: bool = False
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    
    # PDF generation
    PDF_TEMPLATE_DIR: Path = Path("templates/pdf")
    PDF_OUTPUT_DIR: Path = DATA_DIR / "reports" / "pdf"
    
    # Caching
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[Path] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # File upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: list = [".pdf", ".txt", ".docx"]
    
    # Analysis settings
    ANALYSIS_TIMEOUT: int = 300  # 5 minutes
    CONFIDENCE_THRESHOLD: float = 0.7
    
    # Web scraping (future)
    WEB_SCRAPING_ENABLED: bool = False
    REDDIT_API_ENABLED: bool = False
    TWITTER_API_ENABLED: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
