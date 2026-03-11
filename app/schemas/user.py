import re

from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator, ValidationError
from app.models.models import UserRole
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field( min_length =1, max_length=30)
    username: str = Field(min_length=1, max_length=30)
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls,password: str):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", password):
            raise ValueError('Password must contain at least one uppercase letter')
        return password


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

