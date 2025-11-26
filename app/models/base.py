from datetime import datetime, timezone
from functools import partial

from sqlalchemy import (
	DateTime
)
from sqlalchemy.orm import (
	DeclarativeBase,
	Mapped,
	mapped_column,
)


class Base(DeclarativeBase):

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=partial(datetime.now, timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=partial(datetime.now, timezone.utc),
    )
