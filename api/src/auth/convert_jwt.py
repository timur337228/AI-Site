import jwt
import bcrypt
from datetime import timedelta, datetime
from api.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.AUTH_JWT.private_key_path.read_text(),
        algorithm: str = settings.AUTH_JWT.algorithm,
        expire_minutes: int = settings.AUTH_JWT.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()

    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.AUTH_JWT.public_key_path.read_text(),
        algorithms: str = settings.AUTH_JWT.algorithm,
):
    encoded = jwt.decode(token, public_key, algorithms=[algorithms])
    return encoded


def hash_password(
        password: str
) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
        password: str,
        hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password=hashed_password
    )
