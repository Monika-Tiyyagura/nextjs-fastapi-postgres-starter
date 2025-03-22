from fastapi import Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.db_engine import get_db, create_message_db, get_thread_by_id, create_thread_db

messages_router = APIRouter()

class Message(BaseModel):
    content: str

@messages_router.post("/thread/{thread_id}/message", response_model=dict)
async def create_message(thread_id: int, message: Message, db: Session = Depends(get_db)):
    print("Creating message for user")

    create_non_existent_thread(thread_id, db) ## create a thread if the thread id does not exist.
    
    user_message = await create_message_db(thread_id, message.content, True, db)
    
    # Simulating a chatbot response
    bot_response_content = f"You said: {message.content}. Here's a random bot response!"
    bot_message = await create_message_db(thread_id, bot_response_content, False, db)
    
    return {"user": user_message, "bot": bot_message}

async def create_non_existent_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = await get_thread_by_id(thread_id)

    if not thread:
        return await create_thread_db(db)
