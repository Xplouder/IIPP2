# coding=utf-8
# Mini-project #6 - Blackjack
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

__author__ = 'João Silva'

# board definitions
BOARD_SIZE = [600, 600]

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}
ACE_MAX_VALUE = 10


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
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        s = "Hand Contains"
        for card in self.hand:
            s += " " + card.get_suit() + card.get_rank()
        return s

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        value = 0
        aces_count = 0
        for card in self.hand:
            if card.get_rank() == 'A':
                aces_count += 1
            value += VALUES.get(card.get_rank())

        for i in range(aces_count):
            if (value + ACE_MAX_VALUE) > 21:
                break
            value += ACE_MAX_VALUE

        return value

    def draw(self, canvas, pos):
        offset = 0
        for card in self.hand:
            card.draw(canvas, (pos[0] + offset, pos[1]))
            offset += 5 + CARD_SIZE[0]


# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        s = "Deck Contains"
        for card in self.deck:
            s += " " + card.get_suit() + card.get_rank()
        return s


# define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand
    # Deck
    deck = Deck()
    deck.shuffle()
    # Dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "Dealer's " + str(dealer_hand)
    # Player
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    print "Player's " + str(player_hand)

    outcome = "Your Turn :)"
    in_play = True


def hit():
    global player_hand, deck, outcome, in_play

    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted"
            in_play = False
            # TODO -> update  score


def stand():
    global player_hand, dealer_hand, deck, outcome, in_play
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

    if not in_play:
        outcome = "You have busted"
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

        if dealer_hand.get_value() > 21:
            outcome = "You Won!"
            # TODO -> update  score
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "You Lost"
                # TODO -> update  score
            else:
                outcome = "You Won!"
                # TODO -> update  score
    in_play = False


# draw handler
def draw(canvas):
    dealer_hand.draw(canvas, (BOARD_SIZE[0] / 6, CARD_SIZE[1]))
    player_hand.draw(canvas, (BOARD_SIZE[0] / 6, BOARD_SIZE[1] - (CARD_SIZE[1] * 2)))
    canvas.draw_text(outcome, (BOARD_SIZE[0] / 3, BOARD_SIZE[1] / 2), 30, 'White')
    canvas.draw_text("Blackjack", (BOARD_SIZE[0] / 3, BOARD_SIZE[1] / 10), 40, 'White')


# initialization frame
frame = simplegui.create_frame("Blackjack", BOARD_SIZE[0], BOARD_SIZE[1])
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
