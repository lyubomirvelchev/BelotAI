import numpy as np
from project_constants import *
from random_game_generator import construct_random_game_bitarray


class AnnouncementChecker:
    def __init__(self):
        self.ordered_card_values = list(BYTES_TO_CARD_VALUE.keys())

    def evaluate_pre_game_announcements(self, hand):
        pass

    @staticmethod
    def split_hand_by_color(hand):
        cards_split_by_colors = {color: [] for color in BYTES_TO_COLORS.keys()}
        for card_bytes in hand:
            value, color = tuple(card_bytes[:3]), tuple(card_bytes[3:])
            cards_split_by_colors[BYTES_TO_COLORS[color]].append(value)
        return cards_split_by_colors

    @staticmethod
    def split_hand_by_values(hand):
        cards_split_by_values = {card_value: 0 for card_value in BYTES_TO_CARD_VALUE.keys()}
        for card_bytes in hand:
            value = tuple(card_bytes[:3])
            cards_split_by_values[BYTES_TO_CARD_VALUE[value]] += 1
        return cards_split_by_values

    def check_terza_50_100(self, card_values):
        pass

    def check_4_of_a_kind(self, hand):
        for card_bytes in hand:
            value = tuple(card_bytes[:3])
            cards_split_by_values[BYTES_TO_CARD_VALUE[value]] += 1


class GameAnalyzer:
    """TODO: add contra, re contra"""

    def __init__(self, bit_array):
        self.bit_array = bit_array
        self.bit_list = np.array(list(self.bit_array))
        self.points = {
            'TEAM_1': 0,
            'TEAM_2': 0
        }
        self.all_8_deals = np.split(self.bit_list, NUMBER_OF_DEALS)
        self.player_idx = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
        self.player_hands = {
            0: [],
            1: [],
            2: [],
            3: []
        }
        self.announce = "ALL_TRUMP"
        self.team_1_final_cards = []
        self.team_2_final_cards = []
        self.execute_analysis()
        a = 0

    def unpack_single_deal(self, deal):
        first_player_tuple = tuple(deal[:2])
        list_of_4_cards = np.split(deal[2:22], NUMBER_OF_PLAYERS)
        last_player_tuple = tuple(deal[22:24])
        return self.player_idx[first_player_tuple], list_of_4_cards, last_player_tuple

    def get_initial_cards_by_player(self, first_player_idx, cards):
        current_player_idx = first_player_idx
        for idx in range(NUMBER_OF_PLAYERS):
            self.player_hands[current_player_idx].append(cards[idx])
            current_player_idx += 1 if current_player_idx != 3 else -3  # rotation of player index ex.(2, 3, 0, 1)

    def execute_analysis(self):
        deal_idx = 0
        for deal in self.all_8_deals:
            deal_idx += 1
            first_player_idx, cards, last_player = self.unpack_single_deal(deal)
            self.get_initial_cards_by_player(first_player_idx, cards)
            self.calculate_points_from_deal(last_player, cards, True if deal_idx == NUMBER_OF_DEALS else False)

    def check_for_announcements(self):
        pass

    def calculate_points_if_announce_color(self, cards):
        points_deal = 0
        for single_card_bytes in cards:
            current_card_color_bytes = tuple(single_card_bytes[3:])
            if BYTES_TO_COLORS[current_card_color_bytes] == self.announce:
                points_deal += ALL_TRUMP_POINTS[tuple(single_card_bytes[:3])]
            else:
                points_deal += NO_TRUMP_POINTS[tuple(single_card_bytes[:3])]
        return points_deal

    def calculate_points_from_deal(self, last_player, cards, final_10_points):
        team = TEAMS[last_player]
        if self.announce == "ALL_TRUMP":
            points_deal = sum([ALL_TRUMP_POINTS[tuple(single_card_bytes[:3])] for single_card_bytes in cards])
        elif self.announce == 'NO_TRUMP':
            points_deal = sum([NO_TRUMP_POINTS[tuple(single_card_bytes[:3])] for single_card_bytes in cards])
        else:
            points_deal = self.calculate_points_if_announce_color(cards)
        if final_10_points:
            points_deal += 10
        self.points[team] += points_deal


if __name__ == '__main__':
    hui = GameAnalyzer(construct_random_game_bitarray())
