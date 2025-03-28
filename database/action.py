from .base import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Float, UUID
from sqlalchemy.sql import func


class Actions(BaseModel):
    id = Column(UUID, primary_key=True)
    # Time info
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime)
    status = Column(String)
    # Action info
    channel_link = Column(String, nullable=False)
    account_range = Column(Integer, nullable=False)
    mode = Column(String, nullable=False)
    bot_check = Column(Boolean, server_default="False")
    message_check = Column(String)
    answer_check = Column(String)
    boy_girl_ratio = Column(Float)


class ActionsAccounts(BaseModel):
    id = Column(Integer, primary_key=True)
    action_id = Column(UUID, ForeignKey('actions.id', ondelete='CASCADE'), nullable=False)
    account_id = Column(Integer, ForeignKey('telegram_accounts.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


