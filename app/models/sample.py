from datetime import datetime

from beanie import Document, Indexed


class Sample(Document):
    name: Indexed(str)
    createdAt: datetime = datetime.now()
