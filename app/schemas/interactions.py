from pydantic import BaseModel, ConfigDict


class CreateInteraction(BaseModel):
    email: str
    source_id: int
    payload: dict | None = None


class ReadInteraction(BaseModel):
    id: int
    lead_uuid: str
    source_id: int
    operator_id: int | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
