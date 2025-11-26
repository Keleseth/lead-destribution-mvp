from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Interaction


class InteractionCRUD:

    def __init__(
        self,
        model: Interaction
    ):
        self.model = model

    async def get_by_id(
        self,
        session: AsyncSession,
        interaction_id: int,
    ) -> Interaction | None:
        return await session.get(self.model, interaction_id)

    async def create(
        self,
        *,
        session: AsyncSession,
        lead_uuid: str,
        source_id: int,
        operator_id: int | None = None,
        is_active: bool = True,
    ) -> Interaction:
        obj = self.model(
            lead_uuid=lead_uuid,
            source_id=source_id,
            operator_id=operator_id,
            is_active=is_active,
        )
        session.add(obj)
        return obj

    async def set_inactive(
        self,
        session: AsyncSession,
        interaction_id: int,
    ) -> Interaction | None:
        obj = await self.get_by_id(session, interaction_id)
        if obj is None:
            return None
        obj.is_active = False
        return obj

    async def flush(
        self,
        session: AsyncSession,
    ) -> None:
        await session.flush()

    async def commit(
        self,
        session: AsyncSession,
    ) -> None:
        await session.commit()

    async def get_lead_interactions(
        self,
        session: AsyncSession,
        lead_uuid: str,
    ) -> list[Interaction]:
        stmt = select(self.model).where(
            self.model.lead_uuid == lead_uuid
        )
        result = await session.execute(stmt)
        return result.scalars().all()


interaction_crud = InteractionCRUD(Interaction)
