from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseSessionManager:
    def __init__(self):
        self.session_maker = SessionLocal

    async def __aenter__(self):
        self.session = self.session_maker()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

db_manager = DatabaseSessionManager()
