from fastapi import FastAPI
from app.routers import user
from app.database import engine, Base

app = FastAPI()
app.include_router(user.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "FastAPI + PostgreSQL running!"}

