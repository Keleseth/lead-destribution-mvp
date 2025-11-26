from sqlalchemy import (
	Boolean,
	Integer,
	String,
	ForeignKey,
)
from sqlalchemy.orm import (
	Mapped,
	mapped_column,
	relationship
)

from .base import Base


class Lead(Base):
    __tablename__ = 'leads'

    uuid: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        nullable=False,
        unique=True
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    interactions: Mapped[list['Interaction']] = relationship(
        back_populates='lead'
    )

    def __repr__(self) -> str:
        return f'Lead: {self.uuid}'


class Interaction(Base):
    __tablename__ = 'interactions'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    lead_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('leads.uuid'),
        nullable=False
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey('sources.id'),
        nullable=False
    )
    operator_id: Mapped[int | None] = mapped_column(
        ForeignKey('operators.id'),
        nullable=True,
        index=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True
    )

    lead: Mapped['Lead'] = relationship(
        back_populates='interactions'
    )

    def __repr__(self) -> str:
        return f'Interaction: {self.id}'
