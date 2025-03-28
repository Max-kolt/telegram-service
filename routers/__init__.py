from fastapi import APIRouter
from .accounts import accounts_router
from .actions import actions_router


telegram_router = APIRouter(prefix="/v1/telegram")

telegram_router.include_router(accounts_router)
telegram_router.include_router(actions_router)


