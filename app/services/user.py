from typing import Optional
from uuid import UUID
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.enums import TokenType, UserRole
from app.db.session import get_db_session
from app.exceptions.custom_error import InvalidCredentialsError, InvalidTokenError, UserAlreadyExistsError
from app.models.user import User
from app.core.security import security, oauth2_schema
from app.schemas.token import TokenDetails
from app.schemas.user import UserCreate, UserLogin


class UserService:
    """Service for user authentication and management."""

    def __init__(self):
        self.security = security



    async def get_user_by_id(self, user_id: UUID, session: AsyncSession) -> Optional[User]:
        """Retrieve a user by their UUID."""
        return await session.get(User, str(user_id))



    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        """Retrieve a user by their email."""
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalars().first()



    async def create_user(self, user_data: UserCreate, session: AsyncSession) -> User:
        """Create a new user."""
        existing_user = await self.get_user_by_email(user_data.email, session)
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {user_data.email} already exists.")
        user = User(**user_data.model_dump(exclude="password"), hashed_password=self.security.hash_password(user_data.password), role = UserRole.superadmin)

        try:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except IntegrityError as e:
            print(e)
            await session.rollback()
            raise UserAlreadyExistsError(f"User with email {user_data.email} already exists.")


    async def authenticate_user(self, user_data: UserLogin, session: AsyncSession) -> User:
        """Authenticate a user."""
        user = await self.get_user_by_email(user_data.email, session)
        if not user or not self.security.verify_password(user_data.password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password.")
        return user

    async def get_current_user(
        self,
        session: AsyncSession = Depends(get_db_session),
        token: HTTPAuthorizationCredentials = Depends(oauth2_schema)
    ) -> User:
        """
        Retrieve the currently authenticated user.

        Raises:
            InvalidTokenError: If token is invalid or user not found.
        """
        payload = self.security.decode_token(data=TokenDetails(token=token.credentials, token_type=TokenType.ACCESS))
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError("Invalid token payload.")
        user = await self.get_user_by_id(UUID(user_id), session)
        if not user:
            raise InvalidTokenError("User not found for the provided token.")
        print(user)
        return user


user_service = UserService()
