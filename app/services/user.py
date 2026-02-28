from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate):
        return await create_user(self.db, user)

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)