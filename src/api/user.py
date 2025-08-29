from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import SessionLocal
from app.models.schemas import UserCreate, UserOut
from app.services.crud_user import create_user, get_user_by_email

router = APIRouter()

@router.post("/", response_model=UserOut)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user)
