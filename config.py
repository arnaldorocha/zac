"""
Configuration loader for Zac Personal Assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class Config:
    """Application configuration."""
    
    # Load environment variables
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    
    # Voice settings
    VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE", "pt")
    VOICE_ENGINE = os.getenv("VOICE_ENGINE", "pyttsx3")
    VOICE_RATE = int(os.getenv("VOICE_RATE", "150"))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
    
    # Browser settings
    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")
    BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
    
    # Database settings
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/zac.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API settings
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_DEBUG = os.getenv("API_DEBUG", "false").lower() == "true"
    
    # Google Sheets settings
    GOOGLE_SHEETS_CREDENTIALS = os.getenv(
        "GOOGLE_SHEETS_CREDENTIALS",
        "credentials.json"
    )
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")
    
    # Scheduler settings
    SCHEDULER_CHECK_INTERVAL = int(os.getenv("SCHEDULER_CHECK_INTERVAL", "60"))
    
    # Logging settings
    LOG_FILE = os.getenv("LOG_FILE", "logs/zac.log")
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        try:
            # Check essential paths
            Path(cls.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
            Path(cls.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
            
            logger.info("Configuration validated successfully")
            return True
        except Exception as e:
            logger.error(f"Configuration validation error: {e}")
            return False
    
    @classmethod
    def __str__(cls) -> str:
        """String representation."""
        return (
            f"Zac Configuration:\n"
            f"  Voice: {cls.VOICE_LANGUAGE}\n"
            f"  Browser: {cls.BROWSER_TYPE}\n"
            f"  Database: {cls.DATABASE_PATH}\n"
            f"  API: {cls.API_HOST}:{cls.API_PORT}\n"
            f"  Log File: {cls.LOG_FILE}"
        )
