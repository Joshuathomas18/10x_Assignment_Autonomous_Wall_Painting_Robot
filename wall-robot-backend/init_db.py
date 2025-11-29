import asyncio
from app.db.database import engine, Base
from app.db.models import Job

async def init_models():
    async with engine.begin() as conn:
        # This deletes old tables (fresh start) and creates new ones
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print(" Database tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_models())

