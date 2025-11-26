from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead


class LeadCRUD:

	def __init__(
		self,
		model: Lead,
	):
		self.model = model

	async def _get_by_email(
		self,
		session: AsyncSession,
		email: str,
	) -> Lead | None:
		result = await session.execute(
			select(self.model).where(self.model.email == email)
		)
		return result.scalars().first()

	async def get_or_create_by_email(
		self,
		session: AsyncSession,
		email: str,
	) -> Lead:
		lead = await self._get_by_email(session, email)
		if lead is not None:
			return lead
		lead = self.model(
			uuid=str(uuid4()),
			email=email,
		)
		session.add(lead)
		await session.flush()
		return lead


lead_crud = LeadCRUD(Lead)

