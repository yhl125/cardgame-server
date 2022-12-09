from datetime import timedelta

import bcrypt
from fastapi_login import LoginManager

from app.config import settings
from app.models.user import User

manager = LoginManager(settings.access_token_key, token_url='/user/login')


@manager.user_loader()
async def load_user(name: str):
    return await User.find_one(User.name == name)


def create_access_token(data: dict):
    return manager.create_access_token(
        data=data, expires=timedelta(hours=24)
    )


async def create_user(name: str, password: str):
    encrypted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(name=name, password=encrypted_password)
    await user.insert()
    return user


def check_password(password: str, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
