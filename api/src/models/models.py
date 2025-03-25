from sqlalchemy import Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from api.src.models.Base import Base
from sqlalchemy_utils import EmailType, PasswordType


class User(Base):
    username: Mapped[str] = mapped_column(default='Mixx')
    email: Mapped[str] = mapped_column(
        type_=EmailType,
        unique=True,
        index=True,
    )
    password: Mapped[bytes]
    history: Mapped[dict] = mapped_column(JSONB, default=[{}, ])
    available_ai: Mapped[dict] = mapped_column(JSONB, default=[])
    prompts_to_day: Mapped[int] = mapped_column(default=15)
    total_prompts_day: Mapped[int] = mapped_column(default=0)
    token_verified: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    premium: Mapped[dict] = mapped_column(JSONB, nullable=True)
