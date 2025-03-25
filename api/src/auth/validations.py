from jwt.exceptions import InvalidTokenError
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer)
from pydantic import EmailStr

from api.src.auth.email_utils import send_confirm_email
from api.src.auth.helpers_jwt import create_access_token, create_refresh_token
from api.src.auth import convert_jwt as auth_utils
from api.src.auth.schemas import (
    ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD, TokenInfo)
from api.src.models.models import User
from api.src.users.db_func import get_user_by_email, create_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login/")


async def validate_register_auth_user(
        username: str = Form(default="Mixx"),
        email: EmailStr = Form(),
        password: str = Form(),
):
    password = auth_utils.hash_password(password)
    user = await get_user_by_email(email=email, is_verified=False)
    if user:
        if user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User authorized')
            # return await validate_auth_user(email=email, password=password)
    else:
        user = await create_user(username=username, email=email, password=password, is_verified=False)
    await send_confirm_email(user.email, user.username)
    return user


async def validate_auth_user(
        email: EmailStr = Form(),
        password: str = Form(),
):
    unauth_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="invalid username or password")
    user = await get_user_by_email(email)
    if not user:
        raise unauth_exc
    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password
    ) and user.is_verified is False:
        raise unauth_exc
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user is not active")
    return user


def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token error'
        )
    return payload


def is_token_type(payload: dict,
                  token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f'invalid token type {current_token_type!r} expected {token_type!r}')
