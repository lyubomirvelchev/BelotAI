import numpy as np
from project_constants import *


class GameAnalyzer:
    def __init__(self, bit_array):
        self.bit_array = bit_array
        self.bit_list = np.array(list(self.bit_array))
        self.points = {
            'TEAM_1': 0,
            'TEAM_2': 0
        }
        self.all_8_deals = np.split(self.bit_list, HAND_SIZE)
        self.player_idx = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
        self.player_cards = {
            0: [],
            1: [],
            2: [],
            3: []
        }
        self.announce = "ALL_TRUMP"
        self.team_1_final_cards = []
        self.team_2_final_cards = []
        self.get_initial_cards_by_player()

    def unpack_single_deal(self, deal):
        first_player_tuple = tuple(deal[:2])
        list_of_4_cards = np.split(deal[2:22], NUMBER_OF_PLAYERS)
        last_player_tuple = tuple(deal[22:24])
        return self.player_idx[first_player_tuple], list_of_4_cards, last_player_tuple

    def get_initial_cards_by_player(self):
        for deal in self.all_8_deals:
            current_player_idx, cards, last_player = self.unpack_single_deal(deal)
            for idx in range(NUMBER_OF_PLAYERS):
                self.player_cards[current_player_idx].append(cards[idx])
                current_player_idx += 1 if current_player_idx != 3 else -3  # rotation of player index ex.(2, 3, 0, 1)
            self.calculate_points_from_deal(last_player, cards)

    def check_for_announcements(self):
        pass

    def calculate_points_from_deal(self, last_player, cards):
        team = TEAMS[last_player]
        if self.announce == "ALL_TRUMP":
            points = sum([ALL_TRUMP_POINTS[tuple(card[:3])] for card in cards])
        self.points[team] += points


if __name__ == '__main__':
    hui = GameAnalyzer(EXAMPLE_BIT_ARRAY)
