from datetime import datetime
from typing import Optional
from beanie import Document, Indexed


class MotionInput(Document):
    ID: Indexed(str) #ID of the player giving input

    # 베팅 중 사용되는 모션
    # Possible inputs : 1, 2, 3, 4, 5, Q,W,E,R,T, backspace, enter, OK
    bet_chip : Optional[str] = None

    # 게임 중 사용되는 모션
    game : Optional[str] = None 
    # Possible inputs
    # Come : 들어오라는 손짓 (게임 시작)
    # Hit
    # Stand
    # DD (Double Down)

class Menu(Document):
    ID: Indexed(str) #ID of the player
    input : str
    # Possible inputs
    # Balance (잔고 확인)
    # 
