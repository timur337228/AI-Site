from typing import Any

from sqlalchemy.future import select
from fastapi import HTTPException, status
from pydantic import EmailStr
from api.src.models.models import User
from api.src.models.db_client import AsyncSessionLocal
from api.src.redis.redis_helper import get_cached_user, create_cache_user, delete_cache_user, REDIS_IGNORE

unauth_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail="invalid username or password")


async def get_user_by_email(email: EmailStr, active: bool = True, is_verified: bool = True) -> User | None:
    user = await get_cached_user(email)
    if user:
        active_txt = 'active'
        is_verified_txt = 'is_verified'
        if active_txt in user and is_verified_txt in user.keys():
            if user[active_txt] is active and user[is_verified_txt] is is_verified:
                return User(**user)
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User).where(
                User.email == email,
                User.active.is_(active),
                User.is_verified.is_(True) if is_verified else True
            ))
            if result:
                user = result.scalars().first()
                if user:
                    await create_cache_user(user)
                    return user
        except Exception as e:
            # print(e)
            raise unauth_exc
    return


async def get_all_user(active: bool = True) -> list[User] | None:
    async with AsyncSessionLocal() as session:
        if active:
            result = await session.execute(select(User).where(User.active.is_(True)))
        else:
            result = await session.execute(select(User))
        user = result.scalars().all()
    return user


async def update_user(email: str, **kwargs) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if user is None:
                return
            for key, value in kwargs.items():
                if value is not None:
                    setattr(user, key, value)
            print(user.username)
            await create_cache_user(user)
        return user


async def create_user(**data: User) -> User | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = User(**data)
            session.add(user)
            await create_cache_user(user)
            return user


async def get_column_user(column_name: str, email: EmailStr) -> Any:
    user = await get_cached_user(email=email)
    if user:
        if column_name in user:
            return user[column_name]
    user = await get_user_by_email(email)
    await create_cache_user(user)
