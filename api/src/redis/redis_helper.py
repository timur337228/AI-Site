import json
from typing import Any

from pydantic import EmailStr

from api.src.models.models import User
from api.src.users.schemas import USER_COLUMNS
from api.src.redis.redis_client import redis_client

PREFIX_USER = 'user'

REDIS_IGNORE = ('password',)


def create_cache_user_key(email: EmailStr) -> str:
    return f"{PREFIX_USER}_{email}"


async def get_cached_user(email: EmailStr) -> Any:
    if redis_client.redis is not None:
        data = await redis_client.redis.get(create_cache_user_key(email))
        if data:
            user_data = json.loads(data)
            return user_data

    return


async def create_cache_user(user: User):
    model_data = {}
    for i in USER_COLUMNS:
        if i not in REDIS_IGNORE:
            model_data[i] = getattr(user, i)
    await redis_client.redis.set(create_cache_user_key(user.email.lower()), json.dumps(model_data))


async def delete_cache_user(email: EmailStr) -> bool | None:
    try:
        await redis_client.redis.delete(create_cache_user_key(email))
    except:
        return False
    return True
