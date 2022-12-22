########################################################## Blackjack ###########################################################
# -*- coding: utf-8 -*-
# Submitted by : 김세민
# System Requirements: Python 3.8 (Python3)
# 참고 코드 : https://github.com/annaymj/Python-Code/blob/master/Poker.py
################################################################################################################################

#기본적인 틀은 참고 코드 참조, 전체적인 구조는 청우님 
import string, math, random, socket

INT_MAX = 100000000000

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

suits = ("Spades ♠", "Clubs ♣", "Hearts ♥", "Diamonds ♦")
  
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

#카드 클래스
class Card:

  def __init__ (self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __str__ (self):
    return self.rank + " of " + self.suit

  def __eq__ (self, other):
    return (values[self.rank] == values[other.rank])

  def __ne__ (self, other):
    return (values[self.rank] != values[other.rank])

  def __lt__ (self, other):
    return (values[self.rank] < values[other.rank])

  def __le__ (self, other):
    return (values[self.rank] <= values[other.rank])

  def __gt__ (self, other):
    return (values[self.rank] > values[other.rank])

  def __ge__ (self, other):
    return (values[self.rank] >= values[other.rank])
   
#덱 형성
class Deck (object):
  def __init__ (self):
    self.deck = []
    for suit in suits:
      for rank in ranks:
        self.deck.append(Card(suit,rank))
  def __str__(self):
        deck_comp = ""  # start with an empty string
        for card in self.deck:
            deck_comp += "\n " + card.__str__()  # add each Card object's print string
        return "The deck has:" + deck_comp
      
  def shuffle (self):
    random.shuffle (self.deck)

  def __len__ (self):
    return len (self.deck)

  def draw(self):
    if len(self) == 0:
      return None
    else:
      return self.deck.pop(0)

#손패에 카드 추가
class Hand:
  def__init__(self):
    self.cards = []
   
  def add_card(self, card):
    self.cards.append(card)

#게임 중 돈
class Player(Hand):
  def __init__(self, id, money = INT_MAX):
    super().__init__()
    self.id = id
    self.money = money

#청우님 코드 참고
#로그인 하고 아이디에 따른 금액 생성                
class Poker:
  def __init__(self, **player):
    self.num_player = len(player.keys())
    self.players = [] #플레이어 객체들의 리스트
    for id, money in player.items():
        self.players.append(Player(id, money))
        
    # 게임을 하겠다는 의사를 표시
    c = input("포커를 플레이 하시겠습니까? [Y/n] : ")
    while c == "y" or c == "Y" or c == "네":
        self.play()
        c = input("계속하시겠습니까? [Y/n] : ")
    return
  
  #처음 2장 받고 베팅-받고-베팅-받고-베팅-받고-베팅
  def play_draw(self):
      bets = []
      deck = Deck()
      deck.shuffle()
      #각 플레이어들이 먼저 베팅을 한다.
      for player in self.players:
            bets.append(self.make_bet(player))
      
      for i, player in enumerate(self.players):
            player.add_card(deck.draw())
            player.add_card(deck.draw())
            
      for player in self.players:
            bets.append(self.make_bet(player))
       
      for i, player in enumerate(self.players):
            player.add_card(deck.draw())
                 
      for player in self.players:
            bets.append(self.make_bet(player))
                
      for i, player in enumerate(self.players):
            player.add_card(deck.draw())          
                
      for player in self.players:
            bets.append(self.make_bet(player))
            
      for i, player in enumerate(self.players):
            player.add_card(deck.draw())          
                
      for player in self.players:
            bets.append(self.make_bet(player))
  
  #핸드 모션으로 폴드하게 되면 베팅을 멈춘다는 코드가 필요하다
  #
  def make_bet(self,player):
        while True:
            bet = int(input(str(player.id) + "님의 베팅 금액 : "))
            if bet < player.money and bet > 0:
                return bet
            elif bet > player.money:
                print("가진 금액보다 많이 베팅했습니다.")
            elif bet < 1:
                print("더 많이 베팅해야 합니다.")

  #드로우 끝나고 패 까기 
  def play_openhand(self):
    for i in range (len (self.hands) ):
      sortedHand = sorted (self.hands[i], reverse = True)
      hand = ''
      for card in sortedHand:
        hand = hand + str(card) + ' '
      print ('Hand ' + str(i + 1) + ': ' + hand)

  def point(self,hand):                         #point()function to calculate partial score
    sortedHand=sorted(hand,reverse=True)
    c_sum=0
    ranklist=[]
    for card in sortedHand:
      ranklist.append(card.rank)
    c_sum=ranklist[0]*13**4+ranklist[1]*13**3+ranklist[2]*13**2+ranklist[3]*13+ranklist[4]
    return c_sum

      
  def isRoyal (self, hand):               #returns the total_point and prints out 'Royal Flush' if true, if false, pass down to isStraightFlush(hand)
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=10
    Cursuit=sortedHand[0].suit
    Currank=14
    total_point=h*13**5+self.point(sortedHand)
    for card in sortedHand:
      if card.suit!=Cursuit or card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
        print('Royal Flush')
        self.tlist.append(total_point)    
    else:
      self.isStraightFlush(sortedHand)
    

  def isStraightFlush (self, hand):       #returns the total_point and prints out 'Straight Flush' if true, if false, pass down to isFour(hand)
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=9
    Cursuit=sortedHand[0].suit
    Currank=sortedHand[0].rank
    total_point=h*13**5+self.point(sortedHand)
    for card in sortedHand:
      if card.suit!=Cursuit or card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
      print ('Straight Flush')
      self.tlist.append(total_point)
    else:
      self.isFour(sortedHand)

  def isFour (self, hand):                  #returns the total_point and prints out 'Four of a Kind' if true, if false, pass down to isFull()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=8
    Currank=sortedHand[1].rank               #since it has 4 identical ranks,the 2nd one in the sorted listmust be the identical rank
    count=0
    total_point=h*13**5+self.point(sortedHand)
    for card in sortedHand:
      if card.rank==Currank:
        count+=1
    if not count<4:
      flag=True
      print('Four of a Kind')
      self.tlist.append(total_point)

    else:
      self.isFull(sortedHand)
    
  def isFull (self, hand):                     #returns the total_point and prints out 'Full House' if true, if false, pass down to isFlush()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=7
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                 #create a list to store ranks
    for card in sortedHand:
      mylist.append(card.rank)
    rank1=sortedHand[0].rank                  #The 1st rank and the last rank should be different in a sorted list
    rank2=sortedHand[-1].rank
    num_rank1=mylist.count(rank1)
    num_rank2=mylist.count(rank2)
    if (num_rank1==2 and num_rank2==3)or (num_rank1==3 and num_rank2==2):
      flag=True
      print ('Full House')
      self.tlist.append(total_point)
      
    else:
      flag=False
      self.isFlush(sortedHand)

  def isFlush (self, hand):                         #returns the total_point and prints out 'Flush' if true, if false, pass down to isStraight()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=6
    total_point=h*13**5+self.point(sortedHand)
    Cursuit=sortedHand[0].suit
    for card in sortedHand:
      if not(card.suit==Cursuit):
        flag=False
        break
    if flag:
      print ('Flush')
      self.tlist.append(total_point)
      
    else:
      self.isStraight(sortedHand)

  def isStraight (self, hand):
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=5
    total_point=h*13**5+self.point(sortedHand)
    Currank=sortedHand[0].rank                        #this should be the highest rank
    for card in sortedHand:
      if card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
      print('Straight')
      self.tlist.append(total_point)
      
    else:
      self.isThree(sortedHand)
        
  def isThree (self, hand):
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=4
    total_point=h*13**5+self.point(sortedHand)
    Currank=sortedHand[2].rank                    #In a sorted rank, the middle one should have 3 counts if flag=True
    mylist=[]
    for card in sortedHand:
      mylist.append(card.rank)
    if mylist.count(Currank)==3:
      flag=True
      print ("Three of a Kind")
      self.tlist.append(total_point)
      
    else:
      flag=False
      self.isTwo(sortedHand)
        
  def isTwo (self, hand):                           #returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=3
    total_point=h*13**5+self.point(sortedHand)
    rank1=sortedHand[1].rank                        #in a five cards sorted group, if isTwo(), the 2nd and 4th card should have another identical rank
    rank2=sortedHand[3].rank
    mylist=[]
    for card in sortedHand:
      mylist.append(card.rank)
    if mylist.count(rank1)==2 and mylist.count(rank2)==2:
      flag=True
      print ("Two Pair")
      self.tlist.append(total_point)
      
    else:
      flag=False
      self.isOne(sortedHand)
  
  def isOne (self, hand):                            #returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=2
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                       #create an empty list to store ranks
    mycount=[]                                      #create an empty list to store number of count of each rank
    for card in sortedHand:
      mylist.append(card.rank)
    for each in mylist:
      count=mylist.count(each)
      mycount.append(count)
    if mycount.count(2)==2 and mycount.count(1)==3:  #There should be only 2 identical numbers and the rest are all different
      flag=True
      print ("One Pair")
      self.tlist.append(total_point)
      
    else:
      flag=False
      self.isHigh(sortedHand)

  def isHigh (self, hand):                          #returns the total_point and prints out 'High Card' 
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=1
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                       #create a list to store ranks
    for card in sortedHand:
      mylist.append(card.rank)
    print ("High Card")
    self.tlist.append(total_point)
    
def main ():
  game = Poker(id_1=1000, id_2=1200, id_3=1300, id_4=900)
  game.play_draw()          #드로우 하고 베팅 하고
  game.play_openhand()      #끝나면 패 까고

  print('\n')
  for i in range(enumerate(Poker.players)):      #제일 높은 패 찾기
    curHand=game.hands[i]
    print ("Hand "+ str(i+1) + ": " , end="")
    game.isRoyal(curHand)

  maxpoint=max(game.tlist)
  maxindex=game.tlist.index(maxpoint)

  print ('\nHand %d wins'% (maxindex+1))
  
main()
