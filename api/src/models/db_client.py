from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from pydantic import EmailStr

from api.config import settings
from models import User, USER_COLUMNS
from api.src.users.schemas import UserSchema

engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_user_by_email(email: EmailStr):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(
            User.email == email,
            User.active.is_(True)
        ))
        if result:
            user = result.scalars().first()
            return user
        return False


async def get_all_user(active: bool = True):
    async with AsyncSessionLocal() as session:
        if active:
            result = await session.execute(select(User).where(User.active.is_(True)))
        else:
            result = await session.execute(select(User))
        user = result.scalars().all()
        return user


async def update_user(**columns: UserSchema):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            if 'email' not in columns:
                return
            user = await session.get(User, columns["email"])
            if user is not None:
                for i in columns.keys():
                    if i != 'email' and not i is None:
                        setattr(user, i, columns[i])
        return user


async def create_user(**data: UserSchema):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = User(**data)
            session.add(user)