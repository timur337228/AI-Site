from api.config import settings
from api.src.users.schemas import UserSchema
from datetime import timedelta
from api.src.auth import convert_jwt as auth_utils
from api.src.auth.schemas import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE


def create_jwt(
        token_type: str, payload: dict,
        expire_minutes: int = settings.AUTH_JWT.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(payload)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta)


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.email,
        "username": user.username,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        expire_minutes=settings.AUTH_JWT.access_token_expire_minutes, )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        'sub': user.email
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_timedelta=timedelta(days=settings.AUTH_JWT.refresh_token_expire_days))
