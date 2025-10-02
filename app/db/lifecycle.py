from app.db.session import database
from app.db.utils import health_check
from app.core.logging import get_logger

logger = get_logger(__name__)

class DatabaseLifecycle:
    @staticmethod
    async def startup():
        database.create_session_factory()
        if await health_check():
            logger.info("Database connection established successfully")
        else:
            raise RuntimeError("Failed to connect to database")


    @staticmethod
    async def shutdown():
        if database._engine:
            await database._engine.dispose()
            logger.info("Database connections closed")
