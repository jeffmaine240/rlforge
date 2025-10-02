import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy import text
from app.main import app
from app.db.session import database

@pytest.fixture(scope="session")
async def async_test_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.fixture(autouse=True, scope="function")
async def reset_db():
    async with database.get_session() as session:
        await session.execute(text("TRUNCATE TABLE environments RESTART IDENTITY CASCADE;"))
        await session.commit()