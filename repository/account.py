from . import BaseCrudRepo
from database import TelegramAccounts
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update


class TelegramAccountsRepo(BaseCrudRepo):
    model = TelegramAccounts

    @classmethod
    async def get_by_login(cls, db: AsyncSession, login: str) -> TelegramAccounts:
        query = select(cls.model).where(cls.model.login == login)
        return (await db.execute(query)).scalar_one_or_none()

    @classmethod
    async def get_last_range(cls, db: AsyncSession, count: int):
        query = select(cls.model).order_by(cls.model.last_activity.desc()).limit(count)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def update_by_login(cls, db: AsyncSession, login: str, **kwargs):
        query = update(cls.model) \
            .where(cls.model.login == login) \
            .values(**kwargs) \
            .execution_options(synchronize_session='fetch')
        await db.execute(query)
        await db.commit()

    @classmethod
    async def delete_by_login(cls, db: AsyncSession, login: str):
        query = delete(cls.model).where(cls.model.login == login)
        await db.execute(query)
        await db.commit()
