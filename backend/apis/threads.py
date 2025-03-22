from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session

from db.db_engine import get_db, get_threads_db, create_message_db, get_messages_db
from db.models import TextMessage

threads_router = APIRouter()


# Get all Threads
## Add user in input if required.
@threads_router.get("/threads", response_model=list)
async def get_all_threads(db: Session = Depends(get_db)):
    print("Calling threads api")
    return await get_threads_db(db)

# Get Messages by Thread
@threads_router.get("/threads/{thread_id}/messages", response_model=list)
async def get_messages_for_thread(thread_id: int, db: Session = Depends(get_db)):
    print("calling get message for thread id: ", thread_id)
    return await get_messages_db(thread_id, db)