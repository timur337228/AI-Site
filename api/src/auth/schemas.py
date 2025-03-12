from pydantic import BaseModel

TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
