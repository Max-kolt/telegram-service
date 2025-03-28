from datetime import datetime
from typing import Annotated

import jwt
from config import ALGORITHM, SECRET_AUTH_KEY
from fastapi import Depends, HTTPException, Header


async def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_AUTH_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return {}


async def verify_token(access_token: Annotated[str | None, Header()] = None) -> dict:
    if not access_token:
        raise HTTPException(status_code=401, detail="Need authorization header")

    token = access_token.split(' ')[-1]
    payload = await decode_token(token)

    if not {
        "exp", "is_admin", "username", "create_users", "use_func", "manage_tg_accounts", "check_tg_msg"
    }.issubset(payload):
        raise HTTPException(status_code=401, detail='Token damaged')

    if payload["exp"] <= int(datetime.now().timestamp()):
        raise HTTPException(status_code=401, detail='Token expired')

    return payload

everyone_dep = Annotated[dict, Depends(verify_token)]


async def v_is_admin(verify_user: everyone_dep):
    if verify_user['is_admin']:
        return verify_user
    raise HTTPException(status_code=401, detail='User is not admin')

is_admin_dep = Annotated[dict, Depends(v_is_admin)]


async def v_create_users(verify_user: everyone_dep):
    if verify_user['is_admin'] or verify_user['create_users']:
        return verify_user
    raise HTTPException(status_code=401, detail="User can't create users")

can_create_users_dep = Annotated[dict, Depends(v_create_users)]


async def v_use_func(verify_user: everyone_dep):
    if verify_user['is_admin'] or verify_user['use_func']:
        return verify_user
    raise HTTPException(status_code=401, detail="User can't use functions")

can_use_func_dep = Annotated[dict, Depends(v_use_func)]


async def v_manage_tg_accounts(verify_user: everyone_dep):
    if verify_user['is_admin'] or verify_user['manage_tg_accounts']:
        return verify_user
    raise HTTPException(status_code=401, detail="User can't manage telegram accounts")


manage_tg_accounts_dep = Annotated[dict, Depends(v_manage_tg_accounts)]


async def v_check_tg_msg(verify_user: everyone_dep):
    if verify_user['is_admin'] or verify_user['check_tg_msg']:
        return verify_user
    raise HTTPException(status_code=401, detail="User can't check tg msg")


check_tg_msg_dep = Annotated[dict, Depends(v_check_tg_msg)]
