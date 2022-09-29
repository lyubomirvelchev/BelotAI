from project_constants import *
import bitarray
import random


def add_bits_to_bitarray(bits, first_player, current_deal_cards, deal_winner):
    """Extend the bitarray with the new deal bits"""
    bits.extend(first_player)
    for card in current_deal_cards:
        bits.extend(card)
    bits.extend(deal_winner)
    return bits


def construct_random_game_bitarray():
    """Random game with 32 cards and correct order of players. NO RULES APPLIED. TEST PURPOSES ONLY"""
    cards = list(BYTES_TO_CARD.keys())
    random.shuffle(cards)
    players = list(TEAMS.keys())
    game_bits = bitarray.bitarray()  # empty bitarray

    for deal_idx in range(NUMBER_OF_DEALS):
        first_player = random.choice(players) if deal_idx == 0 else deal_winner  # first to play is the last deal winner
        deal_winner = random.choice(players)
        cards, current_deal_cards = cards[:-NUMBER_OF_PLAYERS or None], cards[-4:]
        # remove last 4 cards and assign them to current_deal_cards variable 
        game_bits = add_bits_to_bitarray(game_bits, first_player, current_deal_cards, deal_winner)

    return game_bits


if __name__ == '__main__':
    game_bitarray = construct_random_game_bitarray()  # 24 bytes of unmatched intelligence and sheer mental superiority
    print(game_bitarray)
    print(len(game_bitarray), 'bits')
    print(len(game_bitarray) / 8, 'bytes')
    print('')
    print('24 BYTES OF UNMATCHED INTELLIGENCE AND SHEER MENTAL SUPERIORITY')
