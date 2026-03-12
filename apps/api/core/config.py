from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "QueueForge"
    
    # Configure via .env
    FRONTEND_URL: str
    DATABASE_URL: str
    REDIS_URL: str
    
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    class Config:
        env_file = "../../.env"
        extra = "ignore"

settings = Settings()
