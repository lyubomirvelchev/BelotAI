import bitarray

"""0 equals to 0 and 1 to 1 =>  00101 is 8 of DIAMONDS and 11100 is Ace of CLUBS"""
"""First 3 digits represent the value and the last 2 represent the color"""

TEAMS = {
    (0, 0): 'TEAM_1',
    (0, 1): 'TEAM_2',
    (1, 0): 'TEAM_1',
    (1, 1): 'TEAM_2',
}

ALL_TRUMP_POINTS = {
    (0, 0, 0): 0,
    (0, 0, 1): 0,
    (0, 1, 0): 14,
    (0, 1, 1): 10,
    (1, 0, 0): 20,
    (1, 0, 1): 3,
    (1, 1, 0): 4,
    (1, 1, 1): 11,
}

NO_TRUMP_POINTS = {
    (0, 0, 0): 0,
    (0, 0, 1): 0,
    (0, 1, 0): 0,
    (0, 1, 1): 10,
    (1, 0, 0): 2,
    (1, 0, 1): 3,
    (1, 1, 0): 4,
    (1, 1, 1): 11,
}

CARD_VALUE_TO_BYTES = {
    '7': (0, 0, 0),
    '8': (0, 0, 1),
    '9': (0, 1, 0),
    '10': (0, 1, 1),
    'J': (1, 0, 0),
    'Q': (1, 0, 1),
    'K': (1, 1, 0),
    'A': (1, 1, 1),
}

COLORS_TO_BYTES = {
    'CLUBS': (0, 0),
    'DIAMONDS': (0, 1),
    'HEARTS': (1, 0),
    'SPADES': (1, 1),
}

BYTES_TO_COLORS = {tpl: color for color, tpl in COLORS_TO_BYTES.items()}
BYTES_TO_CARD_VALUE = {tpl: value for value, tpl in CARD_VALUE_TO_BYTES.items()}

NUMBER_OF_DEALS = 8
NUMBER_OF_PLAYERS = 4
NUMBER_OF_CARDS = 32

"""Generate card names dynamically based on dictionary keys"""
CARD_TUPLES = [(value, color) for value in CARD_VALUE_TO_BYTES.keys() for color in COLORS_TO_BYTES.keys()]

"""Generate card bites representation dynamically based on value on color"""
CARD_TO_BYTES = {card: bitarray.bitarray(CARD_VALUE_TO_BYTES[card[0]] + COLORS_TO_BYTES[card[1]]) for card in
                 CARD_TUPLES}
BYTES_TO_CARD = {tuple(bitarray.bitarray(CARD_VALUE_TO_BYTES[card[0]] + COLORS_TO_BYTES[card[1]])): card for card in
                 CARD_TUPLES}

if __name__ == '__main__':
    import pprint

    pprint.pprint(CARD_TO_BYTES)
    pprint.pprint(BYTES_TO_CARD)
