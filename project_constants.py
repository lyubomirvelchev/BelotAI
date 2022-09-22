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

CARD_VALUE = {
    '7': (0, 0, 0),
    '8': (0, 0, 1),
    '9': (0, 1, 0),
    '10': (0, 1, 1),
    'J': (1, 0, 0),
    'Q': (1, 0, 1),
    'K': (1, 1, 0),
    'A': (1, 1, 1),
}

COLORS = {
    'CLUBS': (0, 0),
    'DIAMONDS': (0, 1),
    'HEARTS': (1, 0),
    'SPADES': (1, 1),
}

HAND_SIZE = 8
NUMBER_OF_PLAYERS = 4
NUMBER_OF_CARDS = 32

"""Generate card names dynamically based on dictionary keys"""
CARD_TUPLES = [(value, color) for value in CARD_VALUE.keys() for color in COLORS.keys()]

"""Generate card bites representation dynamically based on value on color"""
CARD_TO_BYTES = {card: bitarray.bitarray(CARD_VALUE[card[0]] + COLORS[card[1]]) for card in CARD_TUPLES}
BYTES_TO_CARD = {tuple(bitarray.bitarray(CARD_VALUE[card[0]] + COLORS[card[1]])): card for card in CARD_TUPLES}
EXAMPLE_BIT_ARRAY = bitarray.bitarray('100101001011110010111101000101001011110010111101'*4)

# EXAMPLE_BIT_ARRAY = bitarray.bitarray('00{}0101{}1111{}0101{}1111{}0000{}1010{}0101{}11'.format())

if __name__ == '__main__':
    import pprint

    pprint.pprint(CARD_TO_BYTES)
    pprint.pprint(BYTES_TO_CARD)
