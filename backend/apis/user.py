from fastapi import APIRouter, HTTPException

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User

class UserRead(BaseModel):
    id: int
    name: str

user_router = APIRouter()

@user_router.get("/users/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        print("Calling backend---")

        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            print("user details : ", result)
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)