import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME = "News API"
    BASE_DIR = Path(__file__).resolve().parent

    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    API_KEY: str = os.getenv("API_KEY")

    # S3 config
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")


    UI_BASE_URL = "https://newsapi.org/v2/everything"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
