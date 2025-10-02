from enum import Enum

class TokenType(str, Enum):
    """Enum for token types."""
    ACCESS = "access"
    REFRESH = "refresh"
    

class EnvironmentEnum(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"


import enum

class UserRole(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"

