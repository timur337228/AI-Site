from jwt.exceptions import InvalidTokenError
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer)

from api.src.users.schemas import UserSchema
from api.src.auth import convert_jwt as auth_utils
from api.src.auth.schemas import (
    ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD)

from api.src.users.db_func import get_user_by_email, create_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jws/login/")


async def validate_register_auth_user(
        username: str = Form(default="Mixx"),
        email: str = Form(),
        password: str = Form(),
):
    print(email, password, username)
    user = await create_user(email=email, username=username, password=password)
    return user


async def validate_auth_user(
        email: str = Form(),
        password: str = Form(),
):
    unauth_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail="invalid username or password")
    if not (user := await get_user_by_email(email)):
        raise unauth_exc
    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password
    ):
        raise unauth_exc
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user is not active")
    return user


def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
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
