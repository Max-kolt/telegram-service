from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID

from database import get_async_session
from repository.action import ActionsRepo
from services.actions import ActionService, ActionSchema, ActionRequestSchema


actions_router = APIRouter(prefix='/actions', tags=['Actions'])


@actions_router.post('/sub_process')
async def start_sub_process(action_data: ActionRequestSchema,
                            db: Annotated[AsyncSession, Depends(get_async_session)]):
    started_action = await ActionService.start_sub_process(db, action_data)
    return started_action


@actions_router.get('/processes')
async def get_processes(db: Annotated[AsyncSession, Depends(get_async_session)]):
    all_processes = await ActionsRepo.get_all(db)
    return all_processes


@actions_router.put('/{process_id}/process_cancel')
async def cancel_process(process_id: str,
                         db: Annotated[AsyncSession, Depends(get_async_session)]):
    cancelled_process = await ActionService.stop_process(db, process_id)
    return cancelled_process


@actions_router.delete('/{process_id}')
async def cancel_process(process_id: str,
                         db: Annotated[AsyncSession, Depends(get_async_session)]):
    cancelled_process = await ActionService.stop_process(db, process_id)
    await ActionsRepo.delete(db, process_id)
    return cancelled_process

