from . import BaseCrudRepo
from database import Actions

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class ActionsRepo(BaseCrudRepo):
    model = Actions

    @classmethod
    async def get_all(cls, db: AsyncSession):
        query = select(cls.model).order_by(cls.model.started_at)
        return (await db.execute(query)).scalars().all()
