import certifi
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models.blackjack import BlackjackGame
from app.models.sample import Sample
from app.models.user import User


async def init_db():
    if settings.env_state == "prod":
        client = AsyncIOMotorClient(settings.mongo_uri, tlsCAFile=certifi.where())
    else:
        client = AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(database=client.cardgame, document_models=[Sample, User, BlackjackGame])
