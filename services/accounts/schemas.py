from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class AuthTelegramAccount(BaseModel):
    login: str
    phone: str
    password: str | None


class ReprTelegramAccount(BaseModel):
    login: str
    phone: str
    user_id: int
    gender: Literal['male', 'female']
    is_active: bool
    online_periods: int | None
    online_delay: int | None
    utc_time: int | None
    created_at: datetime
    updated_at: datetime | None
    last_activity: datetime | None


class AddTelegramAccount(BaseModel):
    user_id: int
    login: str | None
    api_id: int
    api_hash: str
    phone: str
    password: str | None


class ConfirmTelegramAccount(BaseModel):
    user_id: int
    confirm_code: str


class ChangeOnlineSettingsSchema(BaseModel):
    user_id: int
    online_periods: int | None
    online_delay: int | None
    utc_time: int | None

