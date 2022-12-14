from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic import BaseModel

import app.service.user as user_service

router = APIRouter(prefix="/user", tags=["User"])


class UserLoginForm(BaseModel):
    name: str
    password: str


@router.post('/login', response_class=PlainTextResponse)
async def login(data: UserLoginForm):
    name = data.name
    password = data.password

    user = await user_service.load_user(name)
    if not user:
        raise HTTPException(status_code=400, detail='User not exist')
    # elif not user_service.check_password(password, user.password):
    #     raise InvalidCredentialsException

    access_token = user_service.create_access_token(
        data=dict(sub=name)
    )
    return access_token


@router.post('/signup')
async def signup(data: UserLoginForm):
    user = await user_service.load_user(data.name)
    if user:
        raise HTTPException(status_code=400, detail='User already exists')

    return await user_service.create_user(data.name, data.password)


@router.get('/me', response_model=user_service.User)
async def me(user=Depends(user_service.manager)):
    return user


@router.get('/logged_in', response_class=PlainTextResponse)
async def logged_in(user=Depends(user_service.manager)):
    return "If not logged in, you will not see this message"


@router.post('/money/deposit')
async def deposit_money(user=Depends(user_service.manager), amount: int = Body()):
    return await user_service.deposit_money(user, amount)


@router.post('/money/withdraw')
async def withdraw_money(user=Depends(user_service.manager), amount: int = Body()):
    return await user_service.withdraw_money(user, amount)