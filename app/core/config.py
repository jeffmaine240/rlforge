from pydantic_settings import BaseSettings
from app.core.enums import EnvironmentEnum


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEV
    LOG_LEVEL: str = "DEBUG"
    DEBUG: bool = ENVIRONMENT == EnvironmentEnum.DEV

    # Application
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    SECRET_KEY: str

    # Database
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_TYPE: str = "postgresql+asyncpg"

    # Security
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str

    # Mail
    MAIL_FROM_NAME: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    @property
    def database_url(self) -> str:
        return f"{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    # @property
    # def api_base_url(self) -> str:
    #     if self.ENVIRONMENT == EnvironmentEnum.DEV:
    #         return "http://localhost:8000"
    #     elif self.ENVIRONMENT == EnvironmentEnum.STAGING:
    #         return "https://staging.api.hostel-mgt.app"
    #     return "https://api.hostel-mgt.app"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


Config = Settings()
