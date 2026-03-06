from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine
from app.api.user import router as user_router

app = FastAPI()
app.include_router(user_router)


@app.get("/health/db")
async def health_db():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"db": "ok"}
