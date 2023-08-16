import os
from enum import Enum
from typing import Optional

from dotenv import load_dotenv
from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings

load_dotenv(override=True)


class AppEnvironment(Enum):
    """
    Local: Indicates that the application is running on a local machine or environment.
    Development: Indicates that the application is running in a development environment.
    Production: Indicates that the application is running in a production environment.
    Test: Indicates that the application is running in a test environment.
    """

    Local = "Local"
    Development = "Development"
    Production = "Production"


class Settings(BaseSettings):
    """
    A settings class for the project defining all the necessary parameters within the
    app through an object.
    """

    ENV: AppEnvironment = os.getenv("ENV", AppEnvironment.Local)
    APP_NAME: str = os.getenv("APP_NAME")
    APP_VERSION: str = os.getenv("APP_VERSION")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")

    DATABASE_USER: Optional[str] = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: Optional[str] = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST: Optional[str] = os.getenv("DATABASE_HOST")
    DATABASE_PORT: Optional[int] = os.getenv("DATABASE_PORT")
    DATABASE_NAME: Optional[str] = os.getenv("DATABASE_NAME")

    DATABASE_URL: Optional[str] = None

    REDIS_HOST: Optional[str] = os.getenv("REDIS_HOST")
    REDIS_PORT: Optional[int] = os.getenv("REDIS_PORT")

    ACCESS_TOKEN_EXP: int = os.getenv("ACCESS_TOKEN_EXP")
    REFRESH_TOKEN_EXP: int = os.getenv("REFRESH_TOKEN_EXP")
    STRAPI_BASE_URL: str = os.getenv("STRAPI_BASE_URL")
    STRAPI_API_TOKEN: str = os.getenv("STRAPI_API_TOKEN")
    VARIFICATION_LINK_URL: str = os.getenv("VARIFICATION_LINK_URL")

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v, values) -> str:
        """
        Create a Database URL from the settings provided in the .env file.
        """
        if isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.get("DATABASE_USER"),
                password=values.get("DATABASE_PASSWORD"),
                host=values.get("DATABASE_HOST"),
                port=values.get("DATABASE_PORT"),
                path=f"{values.get('DATABASE_NAME')}",
            )
        )


settings = Settings()
