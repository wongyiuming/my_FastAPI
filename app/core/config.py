from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Office-Automation"

    # 强制要求 .env 必须包含以下字段，否则启动报错
    REDIS_URL: str = Field(..., validation_alias="REDIS_URL")
    WALL_ADMIN_TOKEN: str = Field(..., validation_alias="WALL_ADMIN_TOKEN")
    WALL_TTL: int = Field(240, validation_alias="WALL_TTL")  # 默认240秒

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'  # 忽略 env 中无关的变量
    )


settings = Settings()