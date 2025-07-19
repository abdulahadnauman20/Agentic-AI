import os
from typing import Optional

class Config:
    """Configuration class for the Travel Agent System"""
    
    # Gemini API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # Agent Configuration
    MAX_RETRIES: int = 3
    TIMEOUT_SECONDS: int = 30
    
    # Mock Data Configuration
    MOCK_FLIGHTS_ENABLED: bool = True
    MOCK_HOTELS_ENABLED: bool = True
    MOCK_ATTRACTIONS_ENABLED: bool = True
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present"""
        if not cls.GEMINI_API_KEY:
            print("Warning: GEMINI_API_KEY not found in environment variables")
            print("Please set your Gemini API key: export GEMINI_API_KEY='your-api-key'")
            return False
        return True 