from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ActionSchema, ActionRequestSchema
from repository.action import ActionsRepo
from tasks.telegram_actions import sub_process_start, celery_app
from datetime import datetime
from uuid import uuid4, UUID


class ActionService:
    @classmethod
    async def start_sub_process(cls, db: AsyncSession, action_data: ActionRequestSchema) -> ActionSchema:
        action_model = await ActionsRepo.create(db, id=uuid4(), status='processing', **action_data.model_dump(
             include={'channel_link', 'account_range', 'mode', 'bot_check',
                      'message_check', 'answer_check', 'boy_girl_ratio'}
        ))

        sub_process_start.apply_async([action_model.id], task_id=action_model.id)
        return action_model

    @classmethod
    async def stop_process(cls, db: AsyncSession, action_id: str) -> ActionSchema:
        celery_app.control.revoke(str(action_id), terminate=True)
        stopped_process = await ActionsRepo.update(db, action_id, finished_at=datetime.now(), status='stopped')
        return stopped_process


