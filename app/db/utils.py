from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.session import Base, database



async def create_tables():
    engine: AsyncEngine = database.create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def drop_tables():
    engine: AsyncEngine = database.create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



async def health_check() -> bool:
    """
    Database health check
    """
    try:
        from sqlalchemy import text
        async with database.get_session() as session:
            result = await session.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False
