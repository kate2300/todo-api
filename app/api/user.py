from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        data = await service.create_user(user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=UserRead.model_validate(data).model_dump_json())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
