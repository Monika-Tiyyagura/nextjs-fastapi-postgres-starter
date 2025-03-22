from fastapi import Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.db_engine import get_db, create_message_db

messages_router = APIRouter()

class Message(BaseModel):
    content: str

@messages_router.post("/thread/{thread_id}/message", response_model=dict)
async def create_message(thread_id: int, message: Message, db: Session = Depends(get_db)):
    print("Creating message for user")

    user_message = await create_message_db(thread_id, message.content, True, db)
    
    # Simulating a chatbot response
    bot_response_content = f"You said: {message.content}. Here's a random bot response!"
    bot_message = await create_message_db(thread_id, bot_response_content, False, db)
    
    return {"user": user_message, "bot": bot_message}