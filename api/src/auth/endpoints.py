from fastapi import APIRouter, Depends

from api.src.auth.schemas import TokenInfo
from api.src.auth.validations import (
    validate_auth_user,
    validate_register_auth_user,
)
from api.src.auth.utils_jwt import http_bearer, get_current_auth_user_for_refresh, get_current_active_auth_user
from api.src.users.schemas import UserSchema
from api.src.auth.helpers_jwt import create_access_token, create_refresh_token

router = APIRouter(prefix='/jws', tags=['jwt'], dependencies=[Depends(http_bearer)])


def generate_password(user: UserSchema):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )


@router.post('/register/', response_model=TokenInfo)
async def register_auth_user_jwt(
        user: UserSchema = Depends(validate_register_auth_user)
):
    return generate_password(user)


@router.post('/login/', response_model=TokenInfo)
async def auth_user_jwt(
        user: UserSchema = Depends(validate_auth_user)
):
    return generate_password(user)


@router.post("/refresh/", response_model=TokenInfo,
             response_model_exclude_none=True)
def auth_refresh_jwt(
        user: UserSchema = Depends(get_current_auth_user_for_refresh)
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer"
    )


@router.get("/users/me/")
async def auth_user_check_self_info(
        user: UserSchema = Depends(get_current_active_auth_user)
):
    return {
        "username": user.username,
        "email": user.email
    }
