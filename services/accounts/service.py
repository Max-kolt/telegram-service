from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from teleredis import RedisSession
from telethon.tl import functions, types
from telethon import TelegramClient
from fastapi import HTTPException
from loguru import logger
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from telethon.tl.types.auth import SentCode

from utils import telethon_session, telethon_session_decorator
from database.account import TelegramAccounts
from repository.account import TelegramAccountsRepo
from .schemas import AddTelegramAccount, ConfirmTelegramAccount, ChangeOnlineSettingsSchema


class TelegramAccountsService:
    ACCOUNTS_TEMPORARY_STORAGE: dict[int, dict] = {}

    @classmethod
    @telethon_session_decorator
    async def get_face_info(cls, db: AsyncSession, account: TelegramAccounts, client: TelegramClient):
        face_info = await client.get_me()
        full_info: types.UserFull = await client(functions.users.GetFullUserRequest(account.login))

        return {
            'fname': face_info.first_name,
            'lname': face_info.last_name,
            'username': face_info.username,
            'description': full_info.about
        }

    @classmethod
    @telethon_session_decorator
    async def get_user_chats(cls, db: AsyncSession, account: TelegramAccounts, client: TelegramClient):
        to_return = list()
        for chat in client.iter_dialogs(archived=False):
            to_return.append(
                {
                    'id': chat.id,
                    'entity': chat.entity,
                    'last_message': chat.message,
                    'message_date': chat.date,
                    'name': chat.name,
                    'unread_count': chat.unread_count
                }
            )

            return to_return


    @classmethod
    @telethon_session_decorator
    async def get_current_chat(cls, db: AsyncSession, account: TelegramAccounts, client: TelegramClient):
        pass

    @classmethod
    @telethon_session_decorator
    async def change_description(cls, new_description: str,
                                 db: AsyncSession, account: TelegramAccounts, client: TelegramClient):
        await client(functions.account.UpdateProfileRequest(about=new_description))
        return True

    @classmethod
    @telethon_session_decorator
    async def change_fname(cls, new_fname: str,
                           db: AsyncSession, account: TelegramAccounts, client: TelegramClient):
        await client(functions.account.UpdateProfileRequest(first_name=new_fname))
        return True

    @classmethod
    @telethon_session_decorator
    async def change_lname(cls, new_lname: str,
                           db: AsyncSession, account: TelegramAccounts, client: TelegramClient):
        await client(functions.account.UpdateProfileRequest(last_name=new_lname))
        return True

    @classmethod
    async def add_account(cls, db: AsyncSession, account_data: AddTelegramAccount):
        check_account = await TelegramAccountsRepo.get_by_id(db, account_data.user_id)

        try:
            new_account = telethon_session(account_data.user_id, account_data.api_id, account_data.api_hash)
            await new_account.connect()
        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=400, detail="Account values not valid")

        sent_code = await new_account.send_code_request(account_data.phone)
        print(sent_code)
        if not check_account:
            new_account_model = await TelegramAccountsRepo.create(
                db, id=account_data.user_id, login=account_data.login,
                phone=account_data.phone, api_id=account_data.api_id,
                api_hash=account_data.api_hash,
                password=account_data.password)
        else:
            new_account_model = await TelegramAccountsRepo.update(
                db, model_id=account_data.user_id, login=account_data.login,
                phone=account_data.phone, api_id=account_data.api_id,
                api_hash=account_data.api_hash,
                password=account_data.password)

        cls.ACCOUNTS_TEMPORARY_STORAGE[account_data.user_id] = {'account': new_account, 'code_hash': sent_code}
        return new_account_model

    @classmethod
    async def confirm_account(cls, db: AsyncSession, confirm_data: ConfirmTelegramAccount):
        account_model: TelegramAccounts = await TelegramAccountsRepo.get_by_id(db, confirm_data.user_id)
        acc_auth = cls.ACCOUNTS_TEMPORARY_STORAGE.get(confirm_data.user_id)
        if not acc_auth:
            raise HTTPException(400, 'Account not added')
        account: TelegramClient = acc_auth['account']
        code_hash: SentCode = acc_auth['code_hash']

        try:
            await account.sign_in(account_model.phone, confirm_data.confirm_code, phone_code_hash=code_hash.phone_code_hash)
        except SessionPasswordNeededError:
            await account.sign_in(password=account_model.password)
        except PhoneCodeInvalidError as err:
            raise HTTPException(400, err)


        account_profile = await account.get_me()

        result_model = await TelegramAccountsRepo.update(db, confirm_data.user_id, is_active=True,
                                                         login=account_profile.username)
        account.disconnect()
        cls.ACCOUNTS_TEMPORARY_STORAGE.pop(confirm_data.user_id)
        return result_model

    @staticmethod
    async def change_gender(db: AsyncSession, new_gender: int):
        pass

    @staticmethod
    async def change_online_settings(db: AsyncSession, new_settings: ChangeOnlineSettingsSchema):
        pass

    @staticmethod
    async def delete_account(db: AsyncSession, user_id: int):
        await TelegramAccountsRepo.delete(db, user_id)
        return True

