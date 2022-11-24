########################################################## Blackjack ###########################################################
# -*- coding: utf-8 -*-
# Submitted by : 옥청우
# Python script simulates a simple command-line Blackjack game implemented using Python and Object Oriented Programming concepts
# System Requirements: Python 3.8 (Python3)
# 참고 코드 : https://github.com/sheetalbongale/Blackjack-Python/blob/master/README.md
################################################################################################################################

# 입출력을 네트워크로 바꾸고
# split을 구현하여야 한다.
import random
import time
import socket
from flask import Flask

INT_MAX = 2147483647
PlayerBlackjackRate = 1.2
suits = ("Spades ♠", "Clubs ♣", "Hearts ♥", "Diamonds ♦")
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
values = {
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

playing = True

# CLASS DEFINTIONS:


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        #self.value = values[self.rank]

    def __str__(self):
        return self.rank + " of " + self.suit

    def __eq__(self, o):
        return values[self.rank] == values[o.rank]

class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

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
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "A":
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self, inplace = False):
        if inplace:
            while self.value > 21 and self.aces:
                self.value -= 10
                self.aces -= 1
            return self.value
        else:
            value = self.value
            aces = self.aces
            while value > 21 and aces:
                value -= 10
                aces -= 1
            return value

# 플레이를 클래스로 구현
# 여러 플레이어 지원, 각자 클래스
class Player(Hand):
    blackjack = False
    def __init__(self, id, money = INT_MAX):
        super().__init__()
        self.id = id
        self.money = money
    
    def __str__(self):
        comp = ""
        for card in self.cards:
            comp += "\t " + card.__str__()
        return str(self.id)+"님의 패 : "+comp
    def check_blackjack(self):
        self.blackjack == (values[self.cards[0].rank] + values[self.cards[1].rank] == 21)
        return self.blackjack

class play_game:
    # 로그인해서 플레이어 아이디와 가지고 있는 금액을 생성자에 넣는다.
    def __init__(self, **player):
        self.num_player = len(player.keys())
        self.players = [] #플레이어 객체들의 리스트
        for id, money in player.items():
            self.players.append(Player(id, money))
        
        # 게임을 하겠다는 의사를 표시할때까지 기다린다.
        c = input("블랙잭을 플레이 하시겠습니까? [Y/n] : ")
        while c == "y" or c == "Y" or c == "네":
            self.play()
            c = input("계속하시겠습니까? [Y/n] : ")
        return

    def play(self):
        bets = []
        deck = Deck()
        deck.shuffle()
        #각 플레이어들이 먼저 베팅을 한다.
        for player in self.players:
            bets.append(self.make_bet(player))
        
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
            if player.check_blackjack(): break
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
                if player.adjust_for_ace() > 21:
                    print(player)
                    print("플레이어 버스트!")
                    Flag = False
        
        #딜러 차례
        if dealer.check_blackjack(): print("Dealer got a blackjack")
        while dealer.adjust_for_ace() < 17: #Dealer must hit 17
            dealer.add_card(deck.draw())
        print(dealer)

        # 게임 결과
        for i, player in enumerate(self.players):
            print(str(player)+" : "+str((player.adjust_for_ace())))
            if dealer.blackjack and player.blackjack:
                print("Player got blackjack, push")
            elif player.blackjack:
                print("Player got blackjack, win")
                player.money += bet[i]*PlayerBlackjackRate
            elif dealer.blackjack:
                print("Dealer got Blackjack", loose)
                player.money -= bet[i]
            elif player.adjust_for_ace() > 21 and dealer.adjust_for_ace() > 21:
                print("Both Bust")
            elif player.adjust_for_ace() > 21:
                print("Player Bust")
                player.money -= bet[i]
            elif dealer.adjust_for_ace() > 21:
                print("Dealer bust")
                player.money += bet[i]
            elif player.adjust_for_ace() > dealer.adjust_for_ace():
                print("Player Wins!")
                player.money += bet[i]
            elif player.adjust_for_ace() < dealer.adjust_for_ace():
                print("Dealer Wins!")
            else:
                print("Push")
    def make_bet(self, player):
        while True:
            bet = int(input(str(player.id) + "님의 베팅 금액 : "))
            if bet < player.money and bet > 0:
                return bet
        
def main():
    game = play_game(id_1=1000, id_2=1200, id_3=1300, id_4=900)

if __name__ == "__main__":
    main()