# coding=utf-8
# implementation of card game - Memory
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

__author__ = 'João Silva'


def new_game():
    global deck, history, turns_counter
    # card = [number, is_turned, is_discovered]
    deck = [[1, False, False], [2, False, False], [3, False, False], [4, False, False], [5, False, False],
            [6, False, False], [7, False, False], [8, False, False],
            [1, False, False], [2, False, False], [3, False, False], [4, False, False], [5, False, False],
            [6, False, False], [7, False, False], [8, False, False]]
    random.shuffle(deck)
    history = []
    turns_counter = 0


def mouseclick(pos):
    global deck, history, turns_counter
    index = 0

    # Clean the last 2 misses
    if len(history) == 2:
        deck[history[-1]][1] = False
        deck[history[-2]][1] = False
        history = []

    for card in deck:
        card_start = 50 * index
        card_end = 50 * index + 50

        if not card[2] and card_start < pos[0] < card_end:
            if len(history) == 0:  # First Turn
                card[1] = True
                history.append(index)
                turns_counter += 1
                label.set_text("Turns = " + str(turns_counter))
                return
            elif history[-1] != index:  # Second Turn
                if deck[history[-1]][0] == card[0]:  # Hit
                    card[1] = True
                    card[2] = True
                    deck[history[-1]][2] = True
                    history = []
                else:  # Miss
                    card[1] = True
                    history.append(index)
            break
        index += 1


# cards are logically 50x100 pixels in size
def draw(canvas):
    global deck
    (num_pos, num_card) = (20, 0)
    for card in deck:
        canvas.draw_text(str(card[0]), (num_pos, 50), 20, 'White')
        num_pos += 50
        if not card[1]:
            canvas.draw_polygon([(num_card, 0), (num_card, 100), (num_card + 50, 100), (num_card + 50, 0), (0, 0)], 1,
                                'black', 'green')
        else:
            canvas.draw_polygon([(num_card, 0), (num_card, 100), (num_card + 50, 100), (num_card + 50, 0), (0, 0)], 1,
                                'black', None)
        num_card += 50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
