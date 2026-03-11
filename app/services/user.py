from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate):
        try:
            user_object =  await create_user(self.db, user)
            await self.db.commit()
            await self.db.refresh(user_object)
            return user_object
        except IntegrityError as e:
            await self.db.rollback()



def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)