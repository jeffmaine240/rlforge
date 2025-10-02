from typing import Callable, Optional, Dict, Any
from app.core.config import Config



class BaseAppException(Exception):
    """Custom base exception for our app"""
    def __init__(self, message: Optional[str] = None, errors: Optional[Dict[str, Any]] = None):
        self.message = message or f"An error occurred in {Config.APP_NAME}"
        self.errors = errors or {}
        super().__init__(self.message)