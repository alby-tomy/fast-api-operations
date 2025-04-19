from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models import UserProfile
from schemas import UserProfileCreate, UserProfileUpdate

async def get_users(db: AsyncSession):
    result = await db.execute(select(UserProfile))
    return result.scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: int):
    user_details =  await db.get(UserProfile, user_id)
    print("######################",type(user_details))
    if user_details.age is None or user_details.profession is None:
        user_details.is_partial = True
    return user_details
    # result = await db.execute(select(UserProfile).where(UserProfile.id == user_id))  
    
    
async def create_user(db: AsyncSession, user: UserProfileCreate):
    new_user = UserProfile(**user.dict())
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return {
            "id": new_user.id,
            "name": new_user.name,
            "age": new_user.age,
            "email": new_user.email,
            "profession": new_user.profession
        }
    except IntegrityError:
        await db.rollback()
        return None

async def update_user(db: AsyncSession, user_id: int, user: UserProfileCreate):
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        return None
    for key, value in user.dict().items():
        setattr(existing_user, key, value)
    await db.commit()
    await db.refresh(existing_user)
    return existing_user

async def update_user_partial(db: AsyncSession, existing_user, user_update: UserProfileUpdate):
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(existing_user, field, value)  # Update model instance directly

    await db.commit()
    await db.refresh(existing_user)
    return existing_user

async def delete_user(db: AsyncSession, user_id: int):
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        return None
    await db.delete(existing_user)
    await db.commit()
    return existing_user
