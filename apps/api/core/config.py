from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "QueueForge"
    
    # Configure via .env
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/queueforge"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    JWT_SECRET: str = "supersecretjwtkey_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    class Config:
        env_file = ".env"

settings = Settings()
