from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
)


from app.db.config import DatabaseConfig
from app.core.logging import get_logger


logger = get_logger(__name__)

Base = declarative_base()

class AsyncDatabase:
    """
    Async database utilities built on SQLAlchemy.

    - Centralizes engine and session configuration via app.db.config.DatabaseConfig.
    - Creates a cached AsyncEngine with pool tuning (size, overflow, timeouts, recycle, pre-ping) and echo support.
    - Registers DBAPI connection event listeners (connect/checkout/checkin) that log via app.core.logging.get_logger.
    - Provides an async session factory (expire_on_commit=False, autoflush=True).
    - Exposes get_session(), an async context manager that yields an AsyncSession, auto-commits when there are changes, rolls back on error, and always closes.
    - Includes a FastAPI dependency (get_db_session) that yields managed sessions.
    - Exports Base for ORM models.
    """
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    def create_engine(self) -> AsyncEngine:
        if self._engine is not None:
            return self._engine

        self._engine = create_async_engine(
            url=self.config.database_url,
            echo=self.config.echo,
            future=True,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow,
            pool_timeout=self.config.pool_timeout,
            pool_recycle=self.config.pool_recycle,
            pool_pre_ping=self.config.pool_pre_ping,
        )
        self._setup_event_listeners()
        return self._engine

    def _setup_event_listeners(self):
        if not self._engine:
            return

        @event.listens_for(self._engine.sync_engine, "connect")
        def receive_connect(dbapi_connection, connection_record):
            logger.debug("New DBAPI connection established")

        @event.listens_for(self._engine.sync_engine, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            logger.debug("Connection checked out from pool")

        @event.listens_for(self._engine.sync_engine, "checkin")
        def receive_checkin(dbapi_connection, connection_record):
            logger.debug("Connection returned to pool")

    def create_session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is not None:
            return self._session_factory
        
        if self._engine is None:
            self.create_engine()

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=True,
        )
        return self._session_factory

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._session_factory is None:
            self.create_session_factory()
            
        session = self._session_factory()
        try:
            yield session
            if session.dirty or session.new or session.deleted:
                await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


database = AsyncDatabase(DatabaseConfig())


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.get_session() as session:
        yield session
