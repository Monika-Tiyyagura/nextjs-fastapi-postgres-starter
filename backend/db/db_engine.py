from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from db.models import Base, Thread, TextMessage
import random 

_main_uri = "postgres:postgres@localhost:5432/postgres"
_sync_uri = f"postgresql://{_main_uri}"
_async_uri = f"postgresql+asyncpg://{_main_uri}"

sync_engine = create_engine(_sync_uri)
async_engine = create_async_engine(_async_uri)

Base.metadata.create_all(sync_engine)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

async def create_thread_db(db: AsyncSession):
    new_thread = Thread()
    db.add(new_thread)
    await db.commit()
    await db.refresh(new_thread)
    return {"id": new_thread.id}

async def get_threads_db(db: AsyncSession):
    stmt = select(Thread)
    result = await db.execute(stmt)
    return [{"id": thread.id} for thread in result.scalars().all()] if result else []

async def get_thread_by_id(thread_id:int, db: AsyncSession):
    stmt = select(Thread).where(Thread.id == thread_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_message_db(thread_id: int, content: str, added_by_user: bool, db: AsyncSession):
    new_message = TextMessage(
        id=random.randint(0, 2_147_483_647),
        thread_id=thread_id,
        content=content,
        is_request=added_by_user
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    return {
        "id": new_message.id,
        "thread_id": thread_id,
        "content": content,
        "added_by_user": added_by_user,
        "created_timestamp": new_message.created_timestamp,
    }

async def get_messages_db(thread_id: int, db: AsyncSession):
    stmt = select(TextMessage).where(TextMessage.thread_id == thread_id)
    result = await db.execute(stmt)
    return [
        {
            "id": msg.id,
            "content": msg.content,
            "added_by_user": msg.is_request,
            "created_timestamp": msg.created_timestamp,
        }
        for msg in result.scalars().all()
    ] if result else []
