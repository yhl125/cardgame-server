import random

from beanie import PydanticObjectId
from fastapi import HTTPException

from app.models.blackjack import BlackjackGame, BlackjackPlayer, GameStatus, PlayerStatus
from app.models.user import User

PlayerBlackjackRate = 1.5
suits = ("Hearts ♥", "Diamonds ♦", "Spades ♠", "Clubs ♣")
ranks = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
    "A",
)
values_blackjack = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}


# CLASS DEFINTIONS:
# 카드 클래스
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + " of " + self.suit

    def __eq__(self, other):
        return values_blackjack[self.rank] == values_blackjack[other.rank]

    def __ne__(self, other):
        return values_blackjack[self.rank] != values_blackjack[other.rank]

    def __lt__(self, other):
        return values_blackjack[self.rank] < values_blackjack[other.rank]

    def __le__(self, other):
        return values_blackjack[self.rank] <= values_blackjack[other.rank]

    def __gt__(self, other):
        return values_blackjack[self.rank] > values_blackjack[other.rank]

    def __ge__(self, other):
        return values_blackjack[self.rank] >= values_blackjack[other.rank]

    # 왼쪽이 크면 참
    def comp(self, other):
        if values_blackjack[self.rank] != values_blackjack[other.rank]:
            return values_blackjack[self.rank] > values_blackjack[other.rank]
        else:
            return suits.index(self.suit) < suits.index(other.suit)


class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))

    def __str__(self):
        deck_comp = ""  # start with an empty string
        for card in self.deck:
            deck_comp += "\n " + card.__str__()  # add each Card object's print string
        return "The deck has:" + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)


async def create_game(user: User, name: str):
    game = BlackjackGame(name=name)
    player = BlackjackPlayer(name=user.name)
    game.players.append(player)
    return await game.insert()


async def enter_game(user: User, game_id: str):
    game = await BlackjackGame.get(PydanticObjectId(game_id))
    player = BlackjackPlayer(name=user.name)
    # if user not exist in game.players, add user
    if player not in game.players:
        game.players.append(player)
        await game.save()
    else:
        raise HTTPException(status_code=400, detail="already entered")
    return game


async def ready(user: User, game_id: str):
    game = await BlackjackGame.get(PydanticObjectId(game_id))
    if game.status != GameStatus.CREATED and game.status != GameStatus.END:
        raise HTTPException(status_code=400, detail="already started")
    for player in game.players:
        if player.name == user.name:
            player.status = PlayerStatus.READY
            break

    # if all players are ready, start the game
    if all(player.status == PlayerStatus.READY for player in game.players):
        await start_game(game)

    await game.save()
    return await get_game(game_id)


async def start_game(game: BlackjackGame):
    game.status = GameStatus.WAITING_BET
    deck = Deck()
    deck.shuffle()
    game.deck = deck.deck
    for player in game.players:
        player.hand = []
        player.bet = 0
    await game.save()
    return game


async def bet(user: User, game_id: str, bet_money: int):
    if bet_money <= 0:
        raise HTTPException(status_code=400, detail="bet must be more than 0")
    game = await BlackjackGame.get(PydanticObjectId(game_id))
    if game.status != GameStatus.WAITING_BET:
        raise HTTPException(status_code=400, detail="game is not waiting bet")
    for player in game.players:
        if player.name == user.name:
            if user.money < bet_money:
                raise HTTPException(status_code=400, detail="Not enough money")
            player.bet = bet_money
            break
    await draw_card(game_id, user)
    game = await draw_card(game_id, user)
    await game.save()
    if all(player.bet > 0 for player in game.players):
        await dealer_draw_and_wait(game)
    return await get_game(game_id)


async def draw_card(game_id: str, user: User):
    game = await BlackjackGame.get(PydanticObjectId(game_id))
    for player in game.players:
        if player.name == user.name:
            player.hand.append(game.deck.pop())
            break
    await game.save()
    return game


async def draw_card_dealer(game: BlackjackGame):
    game.dealerHand.append(game.deck.pop())
    await game.save()
    return game


async def dealer_draw_and_wait(game: BlackjackGame):
    game.dealerHand.append(game.deck.pop())
    game.dealerHand.append(game.deck.pop())
    game.status = GameStatus.WAITING_CHOICE
    for player in game.players:
        if check_blackjack(player.hand):
            player.status = PlayerStatus.STAND
    await game.save()
    return game


async def stand(user: User, game_id: str):
    game = await BlackjackGame.get(PydanticObjectId(game_id))
    if game.status != GameStatus.WAITING_CHOICE:
        raise HTTPException(status_code=400, detail="game is not waiting choice")
    for player in game.players:
        if player.name == user.name:
            player.status = PlayerStatus.STAND
            break
    if all(player.status == PlayerStatus.STAND for player in game.players):
        while adjust_for_ace(game.dealerHand) < 17:
            await draw_card_dealer(game)
        game = await check_result(game)
    await game.save()
    return await get_game(game_id)


def check_blackjack(hand: list):
    return values_blackjack[hand[0]['rank']] + values_blackjack[hand[1]['rank']] == 21


def adjust_for_ace(hand: list):
    value = 0
    aces = 0
    for card in hand:
        value += values_blackjack[card['rank']]
        if card['rank'] == "A":
            aces += 1  # add to self.aces
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


async def check_result(game: BlackjackGame):
    for player in game.players:
        user: User = await User.find_one(User.name == player.name)
        if check_blackjack(game.dealerHand) and check_blackjack(player.hand):
            print("Player got blackjack, push")
            user.money += player.bet
            player.status = PlayerStatus.PUSH
            user.blackjackPush += 1
        elif check_blackjack(player.hand):
            print("Player got blackjack, win")
            user.money += player.bet * PlayerBlackjackRate * 2
            player.status = PlayerStatus.BLACKJACK
            user.blackjackWins += 1
        elif check_blackjack(game.dealerHand):
            print("Dealer got Blackjack, lose")
            user.money -= player.bet
            player.status = PlayerStatus.LOSE
            user.blackjackLoses += 1
        elif adjust_for_ace(player.hand) > 21 and adjust_for_ace(game.dealerHand) > 21:
            print("Both Bust")
            user.money += player.bet
            player.status = PlayerStatus.BOTH_BUST
            user.blackjackBothBust += 1
        elif adjust_for_ace(player.hand) > 21:
            print("Player Bust")
            user.money -= player.bet
            player.status = PlayerStatus.BUST
            user.blackjackBust += 1
        elif adjust_for_ace(game.dealerHand) > 21:
            print("Dealer bust")
            user.money += player.bet * 2
            player.status = PlayerStatus.WIN
            user.blackjackWins += 1
        elif adjust_for_ace(player.hand) > adjust_for_ace(game.dealerHand):
            print("Player Wins!")
            user.money += player.bet * 2
            player.status = PlayerStatus.WIN
            user.blackjackWins += 1
        elif adjust_for_ace(player.hand) < adjust_for_ace(game.dealerHand):
            print("Dealer Wins!")
            user.money -= player.bet
            player.status = PlayerStatus.LOSE
            user.blackjackLoses += 1
        else:
            print("Push")
            user.money += player.bet
            player.status = PlayerStatus.PUSH
            user.blackjackPush += 1

        await user.save()

    game.status = GameStatus.END
    await game.save()
    return game


# can't view deck, dealer's hand
# can view dealer's first hand
# can view dealer's hand after game is over
async def get_game(game_id: str):
    game = await BlackjackGame.get(PydanticObjectId(game_id))
    game.deck = []
    if game.status != GameStatus.END:
        if len(game.dealerHand) > 0:
            game.dealerHand = [game.dealerHand[0]]
    return game


async def leave_game(user: User, game_id: str):
    game = await BlackjackGame.get(PydanticObjectId(game_id))
    if game.status == GameStatus.CREATED or game.status == GameStatus.END:
        for player in game.players:
            if player.name == user.name:
                game.players.remove(player)
                break
        if all(player.status == PlayerStatus.READY for player in game.players):
            game = await start_game(game)
        await game.save()
    else:
        raise HTTPException(status_code=400, detail="game is not created or end")
    return "successfully left game"


async def hit(user: User, game_id: str):
    await draw_card(game_id, user)
    return await get_game(game_id)


async def find_all_created_game():
    games = await BlackjackGame.find(BlackjackGame.status == GameStatus.CREATED).to_list()
    return games
