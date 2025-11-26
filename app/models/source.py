from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Source(Base):
    __tablename__ = 'sources'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    def __repr__(self) -> str:
        return f'Source: {self.id}'

