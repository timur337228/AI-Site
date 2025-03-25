from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from pathlib import Path

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).parent.parent


class BASE_JWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'


class AuthJWT(BASE_JWT):
    access_token_expire_minutes: int = 10
    refresh_token_expire_days: int = 30


class ConfirmJWT(BASE_JWT):
    access_token_expire_minutes: int = 60


class Settings(BaseSettings):
    KEY_OPENROUTER: str
    EMAIL: str = "official.mixx.ai@gmail.com"
    SMTP: str
    EMAIL_SALT: str
    AUTH_JWT: AuthJWT = AuthJWT()
    CONFIRM_JWT: ConfirmJWT = ConfirmJWT()
    BASE_URL: str = 'https:localhost:3000'
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL_psycopg(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='../.env')


settings = Settings()
