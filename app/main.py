from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine

app = FastAPI()

@app.get("/health/db")
async def health_db():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"db": "ok"}