from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_database_url: str = 'sqlite+aiosqlite:///./app.db'


settings = Settings()