from fastapi import Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer)

from api.src.auth.schemas import TokenInfo
from api.src.auth.validations import is_token_type, get_current_token_payload
from api.src.models.models import User
from api.src.users.db_func import get_user_by_email
from api.src.auth.helpers_jwt import create_access_token, create_refresh_token

http_bearer = HTTPBearer(auto_error=False)


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(payload: dict = Depends(get_current_token_payload)
                                       ) -> User:
        is_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)

    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type('access')
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type('refresh')


async def get_current_active_auth_user(
        user: User = Depends(get_current_auth_user)
):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="user is not active")


async def get_user_by_token_sub(payload: dict) -> User | None:
    email = payload.get('sub')
    if user := await get_user_by_email(email):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='user not found')
