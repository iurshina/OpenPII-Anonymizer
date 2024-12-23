from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./local.db"
    AZURE_API_KEY: str
    AZURE_ENDPOINT: str
    AZURE_ENGINE: str = "gpt-4o-2"
    AZURE_API_VERSION: str = "2024-08-01-preview"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env" 

settings = Settings()
