
from db.seed import seed_user_if_needed

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.messages import messages_router
from apis.threads import threads_router
from apis.user import user_router

app = FastAPI()

app.include_router(threads_router)
app.include_router(messages_router)
app.include_router(user_router)

seed_user_if_needed()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)