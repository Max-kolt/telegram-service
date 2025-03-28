from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from uuid import UUID


class ActionRequestSchema(BaseModel):
    channel_link: str
    account_range: int
    mode: Literal['В течении дня', 'В течении часа', 'Сразу']
    boy_girl_ratio: int
    bot_check: bool
    message_check: str | None
    answer_check: str | None


class ActionSchema(BaseModel):
    id: UUID
    started_at: datetime
    finished_at: datetime | None
    status: Literal['processing', 'finished', 'stopped']
    channel_link: str
    account_range: int
    mode: str
    bot_check: bool
    message_check: str | None
    answer_check: str | None
    boy_girl_ratio: float = Field(1, ge=0, le=1)

