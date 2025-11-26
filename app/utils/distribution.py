import random

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.associations import source_operator_setting_crud


def _operator_choice_by_priority(
    operators: list[dict],
    ) -> int | None:
    if not operators:
        return None
    operator_ids = [int(operator['operator_id']) for operator in operators]
    weights = [max(int(operator['weight']), 0) for operator in operators]
    if sum(weights) == 0:
        weights = [1] * len(operator_ids)
    return random.choices(operator_ids, weights=weights, k=1)[0]


async def select_operator(
    session: AsyncSession,
    source_id: int,
    ) -> int | None:
    operators = await source_operator_setting_crud.get_candidates_for_distribution(
        session=session,
        source_id=source_id,
    )
    return _operator_choice_by_priority(operators)
