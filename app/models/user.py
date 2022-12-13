from datetime import datetime

from beanie import Document, Indexed


class User(Document):
    name: Indexed(str, unique=True)
    password: bytes
    createdAt: datetime = datetime.now()
    money: int = 1000
    blackjackWins: int = 0
    blackjackLoses: int = 0
    blackjackPush: int = 0
    blackjackBlackjack: int = 0
    blackjackBust: int = 0
    blackjackBothBust: int = 0


