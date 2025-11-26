from sqlalchemy import (
	Integer,
	ForeignKey,
	UniqueConstraint
)
from sqlalchemy.orm import (
	Mapped,
	mapped_column
)

from .base import Base


class SourceOperatorSetting(Base):

    __tablename__ = 'source_operator_settings'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey('sources.id'),
        nullable=False
    )
    operator_id: Mapped[int] = mapped_column(
        ForeignKey('operators.id'),
        nullable=False
    )
    weight: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    __table_args__ = (
        UniqueConstraint('source_id', 'operator_id', name='uq_source_operator'),
    )


    def __repr__(self) -> str:
        return f'SourceOperatorSetting: {self.id}'
