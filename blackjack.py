import random
import time
import socket
from flask import Flask
import numpy as np
import copy, re, sys
from argparse import ArgumentParser

INT_MAX = 2147483647
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
#카드 클래스
class Card:
    def __init__ (self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__ (self):
        return self.rank + " of " + self.suit

    def __eq__ (self, other):
        return (values_blackjack[self.rank] == values_blackjack[other.rank])

    def __ne__ (self, other):
        return (values_blackjack[self.rank] != values_blackjack[other.rank])

    def __lt__ (self, other):
        return (values_blackjack[self.rank] < values_blackjack[other.rank])

    def __le__ (self, other):
        return (values_blackjack[self.rank] <= values_blackjack[other.rank])

    def __gt__ (self, other):
        return (values_blackjack[self.rank] > values_blackjack[other.rank])

    def __ge__ (self, other):
        return (values_blackjack[self.rank] >= values_blackjack[other.rank])
    # 왼쪽이 크면 참
    def comp(self, other):
        if values_blackjack[self.rank] != values_blackjack[other.rank]:
            return values_blackjack[self.rank] > values_blackjack[other.rank]
        else: return suits.index(self.suit) < suits.index(other.suit)

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

    def draw(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class

    def add_card(self, card):
        self.cards.append(card)

# 플레이를 클래스로 구현
# 여러 플레이어 지원, 각자 클래스
class Player(Hand):
    def __init__(self, id, money = INT_MAX):
        super().__init__()
        self.id = id
        self.money = money    
    def __str__(self):
        comp = ""
        for card in self.cards:
            comp += "\t " + card.__str__()
        return str(self.id)+"님의 패 : "+comp
    def bet(self):
        while True:
            bet = int(input(str(self.id) + "님의 베팅 금액 : "))
            if bet < self.money and bet > 0:
                self.money -= bet
                return bet
            elif bet > self.money:
                print("가진 금액보다 많이 베팅했습니다.")
            elif bet < 1:
                print("더 많이 베팅해야 합니다.")

class Blackjack:
    # 로그인해서 플레이어 아이디와 가지고 있는 금액을 생성자에 넣는다.
    def __init__(self, **player):
        self.num_player = len(player.keys())
        self.players = [] #플레이어 객체들의 리스트
        for id, money in player.items():
            self.players.append(Player(id, money))

    def play(self):
        bets = []
        deck = Deck()
        deck.shuffle()
        #각 플레이어들이 먼저 베팅을 한다.
        for player in self.players:
            bets.append(player.bet())
        
        #딜러가 먼저 카드 두 장을 뽑는다.
        dealer = Player("dealer")
        dealer.add_card(deck.draw())
        dealer.add_card(deck.draw())
        print("Dealer First Card: " + str(dealer.cards[0]))

        # 플레이어들의 차례
        for i, player in enumerate(self.players):
            Flag = True # stand, double down, blackjack, 21, Bust 시 플레이어 차례 종료 (False)
            player.add_card(deck.draw())
            player.add_card(deck.draw())
            if self.check_blackjack(player): break
            # 각 플레이어의 차례
            while Flag:
                print(player)
                c = input(player.id+"님의 hit (h), double down (d), stand (s) split (sp) 입력하시오 : ")
                if c[0].lower() == "h":
                    player.add_card(deck.draw())
                elif c[0].lower == "d":# and player.money > bets[i]*2:
                    player.add_card(deck.draw())
                    Flag == False
                    bets[i] *= 2
                elif c == "sp" and player.cards[0] == player.cards[1] and len(player.cards)==2 and player.money > bets[i]*2:
                    # 나중에 구현!!!
                    print("Split 되었습니다.")
                elif c[0].lower() == "s":
                    Flag = False
                else :
                    print("유효하지 않은 입력입니다.\n") #어차피 인터페이스 로직은 유니티에서 수행된다. 부자연스러워도 무관
                if self.adjust_for_ace(player) > 21:
                    print(player)
                    print("플레이어 버스트!")
                    Flag = False
        
        #딜러 차례
        if self.check_blackjack(dealer): print("Dealer got a blackjack")
        while self.adjust_for_ace(dealer) < 17: #Dealer must hit 17
            dealer.add_card(deck.draw())
        print(dealer)

        # 게임 결과
        for i, player in enumerate(self.players):
            print(str(player)+" : "+str((self.adjust_for_ace(player))))
            if self.check_blackjack(dealer) and self.check_blackjack(player):
                print("Player got blackjack, push")
                player.money += bets[i]
            elif self.check_blackjack(player):
                print("Player got blackjack, win")
                player.money += bets[i]*PlayerBlackjackRate*2
            elif self.check_blackjack(dealer):
                print("Dealer got Blackjack, loose")
                #player.money -= bets[i]
            elif self.adjust_for_ace(player) > 21 and self.adjust_for_ace(dealer) > 21:
                print("Both Bust")
                player.money += bets[i]
            elif self.adjust_for_ace(player) > 21:
                print("Player Bust")
                #player.money -= bets[i]
            elif self.adjust_for_ace(dealer) > 21:
                print("Dealer bust")
                player.money += bets[i]*2
            elif self.adjust_for_ace(player) > self.adjust_for_ace(dealer):
                print("Player Wins!")
                player.money += bets[i]*2
            elif self.adjust_for_ace(player) < self.adjust_for_ace(dealer):
                print("Dealer Wins!")
            else:
                print("Push")
                player.money += bets[i]
    
    def check_blackjack(self, player):
        return (values_blackjack[player.cards[0].rank] + values_blackjack[player.cards[1].rank] == 21)
    def adjust_for_ace(self, player):
        value = 0
        aces = 0
        for card in player.cards:
            value += values_blackjack[card.rank]
            if card.rank == "A":
                aces += 1  # add to self.aces
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
        
def main():
    game = Blackjack(id_1=1000, id_2=1200, id_3=1300, id_4=900)
    game.play()

if __name__ == "__main__":
    main()