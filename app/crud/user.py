from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    # EmailStr -> str (для типизации и чтобы PyCharm не ругался)
    email_str = str(user_in.email)

    existing = await get_user_by_email(db, email_str)
    if existing:
        raise ValueError("User with this email already exists")

    user = User(
        name=user_in.name,
        username=user_in.username,
        email=email_str,
        password_hash=user_in.password,
    )
    #dhtv временное решение (помогите!!!!!!

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

