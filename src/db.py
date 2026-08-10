from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.config import settings
from src.models import Base, Country

engine = create_async_engine(settings.database, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_countries(data: list[dict]) -> None:
    if not data:
        return
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Country))
        await session.execute(insert(Country).values(data))
        await session.commit()
