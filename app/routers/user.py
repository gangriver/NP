from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.schemas import user as schemas
from typing import List


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[schemas.UserOut])
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    import app.crud
    print("CRUD DIR:", dir(app.crud))
    return await crud.create_user(db, user)
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user