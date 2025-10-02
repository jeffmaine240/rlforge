from fastapi import Depends
from app.core.permissions import Permission
from app.models.user import User
from app.services.user import user_service


async def require_authenticated(user: User = Depends(user_service.get_current_user)) -> User:
    Permission.require_authenticated(user)
    return user


async def require_admin(user: User = Depends(user_service.get_current_user)) -> User:
    Permission.require_admin(user)
    return user


async def require_superadmin(user: User = Depends(user_service.get_current_user)) -> User:
    Permission.require_superadmin(user)
    return user
