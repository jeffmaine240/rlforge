from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr


class RegisteredUserData(BaseModel):
    """Registration schema"""
    uuid: str
    email: EmailStr
    name: str
    is_active: bool
    is_superadmin: bool
    created_at: datetime

    
class UserLogin(BaseModel):
    """UserLogin schema for user login."""
    email: EmailStr
    password: str


class UserCreate(UserLogin):
    """UserCreate schema for creating a new user.

    Args:
        BaseModel (_type_): Base model from Pydantic for data validation.
    """
    name: str


class UserResponse(BaseModel):
    user: RegisteredUserData
    access_token: str