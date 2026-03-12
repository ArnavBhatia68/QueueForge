from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WORKER_ID: str = "worker-default"
    QUEUES_TO_WATCH: str = "default,emails,reports,ml_pipeline"
    POLL_INTERVAL_SEC: float = 1.0
    
    # Configure via .env
    DATABASE_URL: str
    REDIS_URL: str
    
    class Config:
        env_file = "../../.env"
        extra = "ignore"

settings = Settings()
