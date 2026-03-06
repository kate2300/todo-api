from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
