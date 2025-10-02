from datetime import timedelta
from fastapi import Depends, Request, Response, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.core.security import security
from app.core.enums import TokenType
from app.db.session import get_db_session
from app.models import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, RegisteredUserData
from app.schemas.token import TokenCreate, AccessTokenDetails, TokenDetails, Token
from app.services.user import user_service
from app.utils.response import success_response
from app.exceptions.custom_error import InvalidTokenError
from app.core.logging import get_logger
from app.schemas.response import APIResponse

logger = get_logger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=APIResponse[UserResponse])
async def register(user_schema: UserCreate, db: Session  = Depends(get_db_session)):
    user = await user_service.create_user(session=db, user_data=user_schema)

    logger.info(f"User {user.email} registered successfully")

    response = success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=UserResponse(
            user=RegisteredUserData(
                uuid=user.id,
                email=user.email,
                name=user.name,
                is_active=user.is_active,
                is_superadmin=user.is_superadmin,
                created_at=user.created_at
            ),
            access_token=security.create_token(
                token_data=TokenCreate(user_id=user.id, token_type=TokenType.ACCESS)
            )
        ),
    )

    response.set_cookie(
        key="refresh_token",
        value=security.create_token(
            token_data=TokenCreate(user_id=user.id, token_type=TokenType.REFRESH)
        ),
        expires=timedelta(days=60).total_seconds(),
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return response


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=APIResponse[UserResponse])
async def login(request: Request, user_data: UserLogin, db: Session = Depends(get_db_session)):
    user = await user_service.authenticate_user(user_data=user_data, session=db)
    logger.info(f"User {user.email} logged in successfully")

    response = success_response(
        status_code=status.HTTP_200_OK,
        message="Login successful",
        data=UserResponse(
            user=RegisteredUserData(
                uuid=user.id,
                email=user.email,
                name=user.name,
                is_active=user.is_active,
                is_superadmin=user.is_superadmin,
                created_at=user.created_at
            ),
            access_token=security.create_token(
                token_data=TokenCreate(user_id=user.id, token_type=TokenType.ACCESS)
            )
        )
    )

    response.set_cookie(
        key="refresh_token",
        value=security.create_token(
            token_data=TokenCreate(user_id=user.id, token_type=TokenType.REFRESH)
        ),
        expires=timedelta(days=60).total_seconds(),
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return response


@auth_router.post("/refresh-access-token", status_code=status.HTTP_200_OK, response_model=APIResponse[AccessTokenDetails])
async def refresh_access_token(
    request: Request, current_user: User = Depends(user_service.get_current_user)
):
    current_refresh_token = request.cookies.get("refresh_token")
    if not current_refresh_token or not security.is_refresh_token_active(
        token=Token(token=current_refresh_token)
    ):
        logger.warning("Invalid or expired refresh token during refresh attempt")
        raise InvalidTokenError(message="Invalid or expired refresh token")

    access_token, refresh_token = security.refresh_access_token(current_refresh_token=Token(token=current_refresh_token))

    logger.info(f"Token refreshed for user {current_user.id}")

    response = success_response(
        status_code=status.HTTP_200_OK,
        message="Tokens refreshed successfully",
        data=AccessTokenDetails(
            access_token=TokenDetails(
                token=access_token,
                token_type=TokenType.ACCESS
            )
        ),
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=30).total_seconds(),
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return response


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(user_service.get_current_user),
):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        security.redis_client.setex(
            f"blacklisted_token:{refresh_token}", int(timedelta(days=30).total_seconds()), "blacklisted"
        )
        logger.info(f"Refresh token for user {current_user.id} blacklisted")

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
    )

    return success_response(
        status_code=status.HTTP_200_OK,
        message="User logged out successfully",
    )