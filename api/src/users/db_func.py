from typing import Any

from sqlalchemy.future import select
from pydantic import EmailStr
from api.src.models.models import User
from api.src.users.schemas import UserSchema
from api.src.models.db_client import AsyncSessionLocal
from api.src.redis.redis_helper import get_cached_user_column, create_cache_user_column, delete_cache_user_column


async def get_user_by_email(email: EmailStr) -> User | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(
            User.email == email,
            User.active.is_(True)
        ))
        if result:
            user = result.scalars().first()
            return user
    return


async def get_all_user(active: bool = True) -> list[User] | None:
    async with AsyncSessionLocal() as session:
        if active:
            result = await session.execute(select(User).where(User.active.is_(True)))
        else:
            result = await session.execute(select(User))
        user = result.scalars().all()
    return user


async def update_user(redis_add: list = [], **columns: UserSchema) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            if 'email' not in columns:
                return
            user = await session.get(User, columns["email"])
            if user is not None:
                for i in columns.keys():
                    if i != 'email' and not i is None:
                        setattr(user, i, columns[i])
                        if i in redis_add:
                            await create_cache_user_column(column_name=i, email=columns["email"], value=columns[i])
    return user


async def create_user(**data: UserSchema) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = User(**data)
            session.add(user)
            return user


async def get_column_user(column_name: str, email: EmailStr) -> Any:
    column = await get_cached_user_column(column_name=column_name, email=email)
    if not column:
        column = getattr(await get_user_by_email(email), column_name)
        await create_cache_user_column(email=email, column_name=column_name, value=column)
    return column