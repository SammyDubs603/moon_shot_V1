from functools import lru_cache

from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()


class Settings(BaseModel):
    app_password: str = os.getenv("APP_PASSWORD", "change-me")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    coinbase_api_key: str | None = os.getenv("COINBASE_API_KEY")
    coinbase_api_secret: str | None = os.getenv("COINBASE_API_SECRET")
    coinbase_api_host: str = os.getenv("COINBASE_API_HOST", "https://api.coinbase.com")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


@lru_cache
def get_settings() -> Settings:
    return Settings()
