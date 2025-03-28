from .base import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func


class TelegramAccounts(BaseModel):
    id = Column(Integer, nullable=False, primary_key=True, unique=True)  # Telegram ID
    login = Column(String)  # Telegram login
    phone = Column(String, nullable=False, primary_key=True)
    api_id = Column(Integer, nullable=False)
    api_hash = Column(String, nullable=False)
    password = Column(String)

    gender = Column(String)
    is_active = Column(Boolean, default=False)
    online_periods = Column(Integer, default=0)
    online_delay = Column(Integer, default=0)
    utc_time = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    last_activity = Column(DateTime)

