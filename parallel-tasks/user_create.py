from database import SessionLocal
from fastapi import HTTPException
from models import UserProfile

async def create_user_task(user: UserProfileCreate):
    async with SessionLocal() as db:
        new_user = await create_user(db, user)
        if not new_user:
            raise HTTPException(status_code=400, detail=f"Email {user.email} already exists")
        return UserProfile(**new_user)