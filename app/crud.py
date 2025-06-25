from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
import bcrypt

print("crud.py loaded")

async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
