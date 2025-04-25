from typing import Literal

from fastapi import APIRouter, Depends
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from repository.account import TelegramAccountsRepo, TelegramAccounts
from services.accounts import TelegramAccountsService, AddTelegramAccount, ConfirmTelegramAccount, \
    ChangeOnlineSettingsSchema


accounts_router = APIRouter(prefix="/accounts", tags=['Accounts'])


@accounts_router.get('/')
async def get_all(db: AsyncSession = Depends(get_async_session)):
    accounts: list[TelegramAccounts] = await TelegramAccountsRepo.get_all(db)
    return [
        {"id": acc.id,
         "login": acc.login,
         "phone": acc.phone,
         "last_activity": acc.last_activity,
         "created_at": acc.created_at}
        for acc in accounts
    ]


@accounts_router.get('/get_count')
async def get_count(db: AsyncSession = Depends(get_async_session)):
    accounts: list[TelegramAccounts] = await TelegramAccountsRepo.get_all(db)
    return len(accounts)


@accounts_router.get('/{user_id}')
async def get_by_login(user_id: int, db: AsyncSession = Depends(get_async_session)):
    account: TelegramAccounts = await TelegramAccountsRepo.get_by_id(db, user_id)
    return {
        "id": account.id,
        'login': account.login,
        'phone': account.phone,
    }


@accounts_router.get('/{user_id}/face_info')
async def get_face_info(user_id: int,
                        db: AsyncSession = Depends(get_async_session)):
    face_info = await TelegramAccountsService.get_face_info(db, user_id)
    return face_info


@accounts_router.get('/{user_id}/online_info')
async def get_user_online_info(user_id: int,
                               db: AsyncSession = Depends(get_async_session)):
    account: TelegramAccounts = await TelegramAccountsRepo.get_by_id(db, user_id)
    return {
        "periods": account.online_periods,
        "online_delay": account.online_delay
    }


@accounts_router.get('/{user_id}/chats')
async def get_user_chats(user_id: int,
                         db: AsyncSession = Depends(get_async_session)):
    chats = await TelegramAccountsService.get_user_chats

@accounts_router.get('/{user_id}/chat_info')
async def get_user_chat_info(user_id: int,
                             db: AsyncSession = Depends(get_async_session)):
    pass


@accounts_router.post('/add_account')
async def add_account(account_data: AddTelegramAccount,
                      db: AsyncSession = Depends(get_async_session)):
    account_model = await TelegramAccountsService.add_account(db, account_data)
    return account_model


@accounts_router.post('/confirm_account')
async def confirm_account(confirm_data: ConfirmTelegramAccount,
                          db: AsyncSession = Depends(get_async_session)):
    confirmed_account = await TelegramAccountsService.confirm_account(db, confirm_data)
    return confirmed_account


@accounts_router.patch('/{user_id}/change_description')
async def change_description(user_id: int, new_description: str,
                             db: AsyncSession = Depends(get_async_session)):
    return await TelegramAccountsService.change_description(db, user_id, new_description=new_description)


@accounts_router.patch('/{user_id}/change_firstname')
async def change_firstname(user_id: int, new_firstname: str,
                           db: AsyncSession = Depends(get_async_session)):
    return await TelegramAccountsService.change_fname(db, user_id, new_fname=new_firstname)


@accounts_router.patch('/{user_id}/change_lastname')
async def change_lastname(user_id: int, new_lastanme: str,
                          db: AsyncSession = Depends(get_async_session)):
    return await TelegramAccountsService.change_lname(db, user_id, new_lname=new_lastanme)


@accounts_router.patch('/{user_id}/change_gender')
async def change_gender(user_id: int, new_gender: Literal['male', 'female'],
                        db: AsyncSession = Depends(get_async_session)):
    return await TelegramAccountsService.change_gender(db, new_gender)


@accounts_router.patch('/{user_id}/change_online_settings')
async def change_online_settings(user_id: int,
                                 new_settings: ChangeOnlineSettingsSchema,
                                 db: AsyncSession = Depends(get_async_session)):
    return await TelegramAccountsService.change_online_settings(db, user_id, new_settings)


@accounts_router.delete('/delete_account')
async def delete_account(user_id: int, db: AsyncSession = Depends(get_async_session)):
    pass

