import copy
import random

from teams_players import HumanPlayer, AIPlayer
from project_constants import CARD_TUPLES, CARD_BYTES


class Game:
    def __init__(self, players):
        self.PLAYER = {
            1: players[0],
            2: players[1],
            3: players[2],
            4: players[3],
        }
        self.team1 = [self.PLAYER[1], self.PLAYER[3]]
        self.team2 = [self.PLAYER[2], self.PLAYER[4]]
        self.current_player_index = 1  # the player with this index is pod ryka

    def shuffle_deck(self):
        self.deck = copy.deepcopy(CARD_TUPLES)
        random.shuffle(self.deck)

    def deal_cards(self):
        self.shuffle_deck()

        for _ in range(4):
            self.deal_cards_to_current_player(3)
        for _ in range(4):
            self.deal_cards_to_current_player(2)
        """Deal first 5 cards to each player then execute announcement_phase method"""

        self.announcement_phase()

        if "ne vsichki sa PAS":
            for _ in range(4):
                self.deal_cards_to_current_player(3)
            """Deal last 3 card to each player if game is about to be played"""

    def deal_cards_to_current_player(self, number_of_cards):
        """Deal the desired number of cards to the player with the current index"""
        cards = []
        for _ in range(number_of_cards):
            cards.append(self.deal_single_card())
        self.PLAYER[self.current_player_index].current_hand.extend(cards)
        self.change_current_player_index()

    def deal_single_card(self):
        """Also removes the dealt hand from the deck"""
        top_card = self.deck.pop()
        return top_card

    def change_current_player_index(self):
        """Rotate the index from 1 to 4 then 1 and again. This simulates the next player turn"""
        self.current_player_index = self.current_player_index + 1 if self.current_player_index != 4 else 1

    def announcement_phase(self):
        """Here should be the logic of the announces that each player makes (VSICHKO KOZ KURVIII, PAS etc.)"""
        pass


if __name__ == '__main__':
    g = Game([HumanPlayer(), HumanPlayer(), HumanPlayer(), HumanPlayer()])
    g.deal_cards()
    print(g.PLAYER[1].current_hand)
    print(g.PLAYER[2].current_hand)
    print(g.PLAYER[3].current_hand)
    print(g.PLAYER[4].current_hand)
    print(g.deck)
