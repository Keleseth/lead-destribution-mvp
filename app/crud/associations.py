from typing import List, Tuple

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.associations import SourceOperatorSetting
from app.models.operators import Operator


class SourceOperatorSettingCRUD:

    def __init__(
        self,
        model: SourceOperatorSetting,
    ):
        self.model = model

    async def list_by_source(
        self,
        session: AsyncSession,
        source_id: int,
    ) -> List[SourceOperatorSetting]:
        q = select(self.model).where(self.model.source_id == source_id)
        result = await session.execute(q)
        return list(result.scalars().all())

    async def get_candidates_for_distribution(
        self,
        session: AsyncSession,
        source_id: int,
    ) -> List[dict]:
        q = (
            select(
                self.model.operator_id,
                self.model.weight,
            )
            .join(Operator, Operator.id == self.model.operator_id)
            .where(
                self.model.source_id == source_id,
                Operator.active.is_(True),
            )
        )
        result = await session.execute(q)
        rows = result.all()
        return [
            {
                'operator_id': int(op_id),'weight': int(weight)
            } for op_id, weight in rows
        ]

    async def replace_source_weights(
        self,
        session: AsyncSession,
        source_id: int,
        items: List[Tuple[int, int]],
    ) -> None:
        await session.execute(
            delete(self.model).where(self.model.source_id == source_id)
        )
        for op_id, weight in items:
            session.add(self.model(
                source_id=source_id,
                operator_id=op_id,
                weight=weight,
            ))


source_operator_setting_crud = SourceOperatorSettingCRUD(SourceOperatorSetting)
