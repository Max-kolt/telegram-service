from database import BaseModel
from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class BaseCrudRepo:
    model: BaseModel

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        model = cls.model(**kwargs)
        db.add(model)
        await db.commit()
        return model

    @classmethod
    async def update(cls, db: AsyncSession, model_id: str | int, **kwargs):
        query = update(cls.model) \
            .where(cls.model.id == model_id) \
            .values(**kwargs) \
            .execution_options(synchronize_session='fetch').returning(cls.model)
        model = (await db.execute(query)).scalar_one_or_none()
        await db.commit()
        return model

    @classmethod
    async def delete(cls, db: AsyncSession, model_id: str | int):
        query = delete(cls.model).where(cls.model.id == model_id)
        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_all(cls, db: AsyncSession):
        query = select(cls.model)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, model_id: int):
        query = select(cls.model).where(cls.model.id == model_id)
        return (await db.execute(query)).scalar_one_or_none()


class BaseCrudSyncRepo:
    model: BaseModel

    @classmethod
    def create(cls, db: Session, **kwargs):
        model = cls.model(**kwargs)
        db.add(model)
        db.commit()
        return model

    @classmethod
    def update(cls, db: Session, model_id: str | int, **kwargs):
        query = update(cls.model) \
            .where(cls.model.id == model_id) \
            .values(**kwargs) \
            .execution_options(synchronize_session='fetch').returning(cls.model)
        model = db.execute(query).scalar_one_or_none()
        db.commit()
        return model

    @classmethod
    def delete(cls, db: Session, model_id: str):
        query = delete(cls.model).where(cls.model.id == model_id)
        db.execute(query)
        db.commit()

    @classmethod
    def get_all(cls, db: Session):
        query = select(cls.model)
        return db.execute(query).scalars().all()

    @classmethod
    def get_by_id(cls, db: Session, model_id: int):
        query = select(cls.model).where(cls.model.id == model_id)
        return db.execute(query).scalar_one_or_none()
