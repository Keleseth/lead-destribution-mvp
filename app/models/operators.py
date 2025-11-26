from sqlalchemy import Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Operator(Base):
    __tablename__ = 'operators'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
    load_limit: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    def __repr__(self) -> str:
        return f'Operator: {self.id}'
