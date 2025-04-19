from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas import UserProfile, UserProfileCreate, UserProfileUpdate, UserProfileResponse, UserListProfileResponse
from database import get_db, SessionLocal
from crud import get_users, get_user_by_id, create_user, update_user, delete_user, update_user_partial
from asyncio import gather

router = APIRouter()



@router.get("/", response_model=List[UserProfile])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

@router.get("/{user_id}", response_model=UserProfile)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.post("/", response_model=UserListProfileResponse)
async def create_and_fetch_users(users: List[UserProfileCreate], db: AsyncSession = Depends(get_db)):
    async def create_user_task(user: UserProfileCreate):
        async with SessionLocal() as db:
            new_user = await create_user(db, user)
            if not new_user:
                raise HTTPException(status_code=400, detail=f"Email {user.email} already exists")
            return UserProfile(**new_user)

    # Create tasks for creating users
    tasks = [create_user_task(user) for user in users]
    
    # Run tasks in parallel
    created_users = await gather(*tasks)

    return UserListProfileResponse(
        message="Users created successfully",
        user_details=created_users
    )




@router.put("/{user_id}", response_model=UserProfile)
async def update_existing_user(user_id: int, user: UserProfileCreate, db: AsyncSession = Depends(get_db)):
    updated_user = await update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.patch("/{user_id}", response_model=UserProfile)
async def partial_update_user(user_id: int, user_update: UserProfileUpdate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_update.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    updated_user = await update_user_partial(db, existing_user, user_update)  # Pass model object
    return updated_user

@router.delete("/{user_id}")
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted_user = await delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
