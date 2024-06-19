import os
from typing import Any, Dict, Optional

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,
        "pool_recycle": 1800,
    }

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_uri(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        values = info.data
        return f"mysql+pymysql://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}:{values.get('DB_PORT')}/{values.get('DB_DATABASE')}"


class Settings(DBSettings):
    """
    Basic Settings
    """

    ENV: str = "local"
    API_VERSION: str = "v1"


def get_settings() -> Settings:
    configs = {
        "migration": DBSettings,
        "local": Settings,
    }
    return configs.get(os.getenv("ENV", "local"))()


settings = get_settings()
