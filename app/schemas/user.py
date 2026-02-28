from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.models import UserRole
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

