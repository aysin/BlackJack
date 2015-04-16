# Mini-project #6 - Blackjack
# Aysin Oruz

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or Stand"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cardList = []
        

    def __str__(self):
        # return a string representation of a hand
        x = "Hand contains: "
        for i in self.cardList: 
            x += str(i) + " "
        return x

    def add_card(self, card):
        # add a card object to a hand
        self.cardList.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        aces = 0
        if len(self.cardList) == 0: 
            return value
        for i in range(0, len(self.cardList)):
            a = self.cardList[i].get_rank()
            value += VALUES[a]
            if a == 'A': aces += 1
        if (aces > 0) and (value + 10 <= 21):
            value += 10
        return value
   
    def draw(self, canvas, p):
        for i in self.cardList:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(i.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(i.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [p[0] + CARD_CENTER[0] + 73 * self.cardList.index(i), p[1] + CARD_CENTER[1]], CARD_SIZE)
            
     
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cardList = []
        for i in SUITS:
            for j in RANKS:
                cardx = Card(i, j)
                self.cardList.append(cardx)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cardList)
        

    def deal_card(self):
        # deal a card object from the deck
        x = self.cardList.pop()
        return x
    
    def __str__(self):
        # return a string representing the deck
         # return a string representation of a hand
        x = "Hand contains: "
        for i in self.cardList: 
            x += str(i) + " "
        return x



#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score
    
    if in_play == False:
        deck = Deck()
        player = Hand()
        dealer = Hand()
        deck.shuffle()
        for i in range(2):
            dealer.add_card(deck.deal_card())
            player.add_card(deck.deal_card())
        dealer.cardList[0].hidden = True
        outcome = "Hit or Stand?"
        in_play = True
    else:
        outcome = "Restared the game!"
        score -= 1
        in_play = False 

def hit():
    # replace with your code below
    global player, in_play, score, outcome
 
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            outcome = "You have Busted!"
            in_play = False
            score -= 1
        
       
def stand():
    # replace with your code below
    global in_play, outcome, player, dealer, score
   
    if not in_play: return 
    
    if player.get_value() > 21:
        outcome = "You have Busted!"
        score -= 1
    else:
        while dealer.get_value() < 17:
            d = deck.deal_card()
            dealer.add_card(d)
    if dealer.get_value() > 21:
        outcome = "Dealer has busted! New Game?"
        score += 1
    else: 
        if player.get_value() > dealer.get_value():
            outcome = "You Win! New Game!?"
            score += 1
        else: 
            outcome = "You Lose! New Game?"
            score -= 1
  
    # assign a message to outcome, update in_play and score
    in_play = False 

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Black Jack", [220, 100], 36, "Black")
    canvas.draw_text(str(outcome), [0, 200], 30, "Black")
    canvas.draw_text("Score: " + str(score), [255,150], 30, "Black")
    canvas.draw_text("Player", (8, 390), 30, "Black")
    canvas.draw_text("Dealer", (8, 290), 30, "Black")
    dealer.draw(canvas, [100, 250])
    player.draw(canvas, [100, 350])
    player.draw(canvas, [100, 350])



    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [174 + CARD_BACK_CENTER[0], 250 + CARD_BACK_CENTER[1]], CARD_SIZE)  


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)



# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
