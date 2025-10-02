from fastapi import HTTPException, status
from app.models.user import User


class Permission:
    
    @staticmethod
    def require_superadmin(user: User):
        if not user.is_superadmin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Superadmin privileges required."
            )

    @staticmethod
    def require_admin(user: User):
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required."
            )

    @staticmethod
    def require_authenticated(user: User):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required."
            )
