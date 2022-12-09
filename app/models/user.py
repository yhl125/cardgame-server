from datetime import datetime

from beanie import Document, Indexed


class User(Document):
    name: Indexed(str, unique=True)
    password: bytes
    createdAt: datetime = datetime.now()
