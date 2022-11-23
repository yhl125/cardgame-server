from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from models.sample import Sample


async def init_db():
    client = AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(database=client.cardgame, document_models=[Sample])
