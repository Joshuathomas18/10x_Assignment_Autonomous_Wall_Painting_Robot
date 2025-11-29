from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# DB connection string - using async sqlite driver
DATABASE_URL = "sqlite+aiosqlite:///./robot_missions.db"

# Engine setup
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    future=True
)

# Session factory for request-scoped sessions
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

# FastAPI dependency - yields session and auto-closes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

