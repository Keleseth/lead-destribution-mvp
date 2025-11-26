from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.interactions import interaction_crud
from app.db.db_dependencies import get_async_session
from app.models.lead import Interaction


async def get_interactions_by_lead_uuid(
	lead_uuid: str,
	session: AsyncSession = Depends(get_async_session),
) -> list[Interaction]:
	items = await interaction_crud.get_lead_interactions(
		session=session,
		lead_uuid=lead_uuid
    )
	return items
