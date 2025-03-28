from functools import wraps
from types import FunctionType
from typing import Annotated, Any, Callable

from redis import Redis
from teleredis import RedisSession
from telethon import TelegramClient
from sqlalchemy.ext.asyncio import AsyncSession
from repository.account import TelegramAccountsRepo
from config import REDIS_HOST, REDIS_USER, REDIS_PORT, REDIS_PASSWORD, REDIS_DB_SESSIONS


def telethon_session(user_id: int, api_id: int, api_hash: str) -> TelegramClient:
    redis_connector = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB_SESSIONS,
                            decode_responses=False)
    session = RedisSession(f'session_{user_id}', redis_connector)
    return TelegramClient(session, api_id=api_id, api_hash=api_hash)


def telethon_session_decorator(func):
    @wraps(func)
    async def wrapper(cls, db: AsyncSession, user_id: int, *args, **kwargs):
        print(db, user_id)
        acc_info = await TelegramAccountsRepo.get_by_id(db, user_id)
        api_id, api_hash = acc_info.api_id, acc_info.api_hash

        tg_client = telethon_session(user_id, api_id, api_hash)

        await tg_client.start()

        func_result = await func(cls, db=db, client=tg_client, account=acc_info, *args, **kwargs)
        tg_client.disconnect()

        return func_result

    return wrapper
