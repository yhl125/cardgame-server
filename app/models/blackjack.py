from datetime import datetime
from enum import Enum

from beanie import Document, Indexed
from pydantic import BaseModel


class PlayerStatus(str, Enum):
    ENTER = "enter"
    READY = "ready"
    STAND = "stand"
    WIN = "win"
    LOSE = "lose"
    PUSH = "push"
    BLACKJACK = "blackjack"
    BUST = "bust"
    BOTH_BUST = "both_bust"


class BlackjackPlayer(BaseModel):
    name: Indexed(str)
    hand: list = []
    bet: int = 0
    status: PlayerStatus = PlayerStatus.ENTER


class GameStatus(str, Enum):
    CREATED = "created"
    WAITING_BET = "waiting_bet"
    WAITING_CHOICE = "waiting_choice"
    END = "end"


class BlackjackGame(Document):
    players: list[BlackjackPlayer] = []
    deck: list = []
    dealerHand: list = []
    status: Indexed(str) = GameStatus.CREATED
    playedCount: int = 0
    createdAt: datetime = datetime.now()
