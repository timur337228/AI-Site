from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


# class CreateUser(BaseModel):
#     email: EmailStr
#     username: Annotated[str, MinLen(3), MaxLen(20)]
#

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: Annotated[str, MinLen(3), MaxLen(20)] = "Mixx"
    email: EmailStr
    password: bytes
    history: list = [{}, ]
    available_ai: list = []
    prompts_to_day: int = 15
    total_prompts_day: int = 0
    premium: dict | None = None
    active: bool = True


USER_COLUMNS = list(UserSchema.model_fields.keys())
