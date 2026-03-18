from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="Colonie Vacances 2026 - API", alias="APP_NAME")
    environment: str = Field(default="dev", alias="ENVIRONMENT")

    database_url: str = Field(alias="DATABASE_URL")

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=120, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    cors_allow_origins: str = Field(default="", alias="CORS_ALLOW_ORIGINS")

    smtp_host: str = Field(default="", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_username: str = Field(default="", alias="SMTP_USERNAME")
    smtp_password: str = Field(default="", alias="SMTP_PASSWORD")
    smtp_from: str = Field(default="", alias="SMTP_FROM")

    def cors_origins_list(self) -> List[str]:
        if not self.cors_allow_origins:
            return []
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

