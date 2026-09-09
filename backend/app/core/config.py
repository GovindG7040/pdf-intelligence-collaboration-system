from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# E:\PDF Intelligence & Collaboration System
BASE_DIR = Path(__file__).resolve().parents[3]

ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///../pdf_intelligence.db"

    SECRET_KEY: str = "change-this-in-production"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    GEMINI_API_KEY: str = ""

    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()