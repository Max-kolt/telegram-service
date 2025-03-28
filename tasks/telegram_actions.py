from .config import celery_app, session_maker, logger
from database.action import Actions, ActionsAccounts
from database.account import TelegramAccounts
from repository import BaseCrudSyncRepo
from utils import telethon_session

from sqlalchemy.orm import Session
from sqlalchemy import select
from telethon.tl import functions
from telethon import TelegramClient
from teleredis import RedisSession
from redis import Redis
from asgiref.sync import async_to_sync
from typing import Literal
import math
import random
import time
import datetime
import asyncio


class ActionRepo(BaseCrudSyncRepo):
    model = Actions


class ActionAccountRepo(BaseCrudSyncRepo):
    model = ActionsAccounts


class TelegramAccountsRepo(BaseCrudSyncRepo):
    model = TelegramAccounts

    @classmethod
    def get_by_gender(cls, db: Session, gender: Literal['female', 'male'] = None, limit: int = None):
        query = select(cls.model).where(cls.model.gender == gender).order_by(cls.model.last_activity)
        if limit:
            query = query.limit(limit)

        return db.execute(query).scalars().all()



@celery_app.task()
def sub_process_start(action_id: int):
    with session_maker() as session:
        action: Actions = ActionRepo.get_by_id(session, action_id)

    duration: int = {
        'В течении дня': 240*60*60,
        'В течении часа': 60*60,
        'Сразу': 1
    }[action.mode]

    delay_between_activities = duration / action.account_range

    boys_count, girls_count = int(action.account_range * action.boy_girl_ratio), \
        math.ceil(action.account_range * (1-action.boy_girl_ratio))

    with session_maker() as session:
        girl_accounts = TelegramAccountsRepo.get_by_gender(session, 'female', limit=girls_count)
        boy_accounts = TelegramAccountsRepo.get_by_gender(session, 'male', limit=boys_count)

        result_count = len([*girl_accounts, *boy_accounts])
        accounts: list[TelegramAccounts] = [*girl_accounts, *boy_accounts]

        if result_count < action.account_range:
            accounts = [*TelegramAccountsRepo.get_by_gender(session, limit=girls_count), *accounts]

    random.shuffle(accounts)

    logger.info(f"Starting subscription process {action_id}: \n{accounts}")
    async_to_sync(run_subscription)(accounts, action, delay_between_activities)

    with session_maker() as session:
        ActionRepo.update(session, model_id=action_id, status='finished', finished_at=datetime.datetime.now())

        logger.info(f"Finishing subscription process {action_id}")


async def run_subscription(accounts: list[TelegramAccounts], action: Actions, delay: float):
    for acc in accounts:
        time.sleep(delay)
        t_acc = telethon_session(acc.id, acc.api_id, acc.api_hash)
        await t_acc.start()

        try:
            await t_acc(functions.channels.JoinChannelRequest(action.channel_link.split('/')[-1]))
        except Exception:
            await t_acc(functions.messages.ImportChatInviteRequest(hash=action.channel_link.split('/')[-1].strip('+')))

        logger.info(f'Sending invite request to group [{acc.id}]')

        if action.bot_check:
            for attempt in range(1, 6):
                time.sleep(5)
                dialogs = await t_acc.get_dialogs(archived=False, limit=10)
                current_dialog = None

                for d in dialogs:
                    messages = [message.message.lower()
                                for message in await t_acc.get_messages(d) if isinstance(message.message, str)]
                    if action.message_check.format(username=acc.login, userid=acc.id).lower() in messages:
                        current_dialog = d
                        break

                if current_dialog:
                    time.sleep(2)
                    await t_acc.send_message(current_dialog,
                                             action.answer_check.format(
                                                 username=acc.login, userid=acc.id
                                             ))
                    logger.info('Answered on bot checking question')
                    break

                logger.info(f'Attempt {attempt} for listening bot checking question')

        await t_acc.disconnect()

        logger.info(f'Disconnect account [{acc.id}]')

        with session_maker() as session:
            ActionAccountRepo.create(session, action_id=action.id, account_id=acc.id)
            TelegramAccountsRepo.update(session, model_id=acc.id, last_activity=datetime.datetime.now())

        logger.info(f'Update activity info about account [{acc.id}]')
