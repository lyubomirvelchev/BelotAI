import bitarray

"""False equals to 0 and True to 1 =>  00101 is 8 of DIAMONDS and 11100 is Ace of CLUBS"""
"""First 3 digits represent the value and the last 2 represent the color"""

CARD_VALUE = {
    '7': [False, False, False],
    '8': [False, False, True],
    '9': [False, True, False],
    '10': [False, True, True],
    'J': [True, False, False],
    'Q': [True, False, True],
    'K': [True, True, False],
    'A': [True, True, True],
}

COLORS = {
    'CLUBS': [False, False],
    'DIAMONDS': [False, True],
    'HEARTS': [True, False],
    'SPADES': [True, True],
}

HAND_SIZE = 8
NUMBER_OF_PLAYERS = 4
NUMBER_OF_CARDS = 32

"""Generate card names dynamically based on dictionary keys"""
CARD_TUPLES = [(value, color) for value in CARD_VALUE.keys() for color in COLORS.keys()]

"""Generate card bites representation dynamically based on value on color"""
CARD_BYTES = {card: bitarray.bitarray(CARD_VALUE[card[0]] + COLORS[card[1]]) for card in CARD_TUPLES}

if __name__ == '__main__':
    import pprint

    pprint.pprint(CARD_BYTES)
