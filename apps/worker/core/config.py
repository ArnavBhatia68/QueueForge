from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WORKER_ID: str = "worker-default"
    QUEUES_TO_WATCH: str = "default,emails,reports,ml_pipeline"
    POLL_INTERVAL_SEC: float = 1.0
    
    # Configure via .env
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/queueforge"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"

settings = Settings()
