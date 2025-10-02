
from typing import Any, Dict, Optional
from app.exceptions.base import BaseAppException



class UserAlreadyExistsError(BaseAppException):
    """Exception raised when trying to create a user that already exists."""
    def __init__(self, message: str = "User already exists", errors: Optional[Dict[str, Any]] = None):
        super().__init__(message, errors)
        

class InvalidCredentialsError(BaseAppException):
    """Exception raised for invalid user credentials."""
    def __init__(self, message: str = "Invalid credentials provided", errors: Optional[Dict[str, Any]] = None):
        super().__init__(message, errors)
        


class InvalidTokenError(BaseAppException):
    """Exception raised for invalid or expired tokens."""
    def __init__(self, message: str = "Invalid or expired token", errors: Optional[Dict[str, Any]] = None):
        super().__init__(message, errors)



class ServerError(BaseAppException):
    """Exception raised for server failure."""
    def __init__(self, message: str = "Server Error", errors: Optional[Dict[str, Any]] = None):
        super().__init__(message, errors)
