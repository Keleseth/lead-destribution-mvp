from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.interactions import interaction_crud
from app.crud.lead import lead_crud
from app.db.db_dependencies import get_async_session
from app.schemas.interactions import (
    CreateInteraction,
    ReadInteraction,
)
from app.api.dependencies import get_interactions_by_lead_uuid
from app.utils.distribution import select_operator


router = APIRouter()


@router.post(
    '/interaction',
    status_code=status.HTTP_201_CREATED,
    response_model=ReadInteraction,
    )
async def intake_interaction(
    body: CreateInteraction,
    session: AsyncSession = Depends(get_async_session),
) -> ReadInteraction:
    lead = await lead_crud.get_or_create_by_email(
        session=session,
        email=body.email,
    )
    operator_id = await select_operator(session=session, source_id=body.source_id)
    interaction = await interaction_crud.create(
        session=session,
        lead_uuid=lead.uuid,
        source_id=body.source_id,
        operator_id=operator_id,
        is_active=True,
    )
    await interaction_crud.flush(session=session)
    await interaction_crud.commit(session=session)
    return interaction


@router.get(
    '/leads/{lead_uuid}/interactions',
    response_model=list[ReadInteraction]
    )
async def get_lead_interactions(
    items: list[ReadInteraction] = Depends(get_interactions_by_lead_uuid),
):
    return items
