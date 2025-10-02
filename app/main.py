from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware



from app.core.config import Config
from app.api.v1.routers import router
from app.exceptions.custom_error import InvalidCredentialsError, InvalidTokenError, UserAlreadyExistsError, ServerError
from app.exceptions.exception_handler import create_exception_handler

app = FastAPI(title=Config.APP_NAME)

@app.get("/config")
def read_config():
    return {
        "app_name": Config.APP_NAME,
        "db_user": Config.DB_USER,
        "redis_host": Config.REDIS_URL
    }


app.include_router(router, prefix="/api")
app.add_middleware(SessionMiddleware, secret_key=Config.SECRET_KEY)

app.add_exception_handler(
    exc_class_or_status_code=InvalidCredentialsError,
    handler=create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        default_message="Invalid credentials provided."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidTokenError,
    handler=create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        default_message="Invalid or expired token."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=ServerError,
    handler=create_exception_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        default_message="Internal Server Error"
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=UserAlreadyExistsError,
    handler=create_exception_handler(
        status_code=status.HTTP_409_CONFLICT,
        default_message="A user with this email already exists."
    ),
)

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
