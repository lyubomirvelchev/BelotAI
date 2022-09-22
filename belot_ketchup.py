import copy
import random
from secrets import randbelow
import time

from teams_players import HumanPlayer, AIPlayer
from project_constants import *


class Game:
    def __init__(self, players):
        self.PLAYER = {idx: players[idx] for idx in range(4)}
        self.team1 = [self.PLAYER[0], self.PLAYER[2]]
        self.team2 = [self.PLAYER[1], self.PLAYER[3]]
        self.current_player_idx = 0  # the player with this index is pod ryka
        self.played_cards = []
        self.current_deal = []
        self.played_deals = []
        self.announce = ''
        self.played_deals_count = 0
        self.first_deals_combinations = []  # TODO variable pollution
        self.second_deal_combinations = []  # variables for  saving played cards by algorithm
        self.remaining_cards = []

    def shuffle_deck(self):
        self.deck = copy.deepcopy(CARD_TUPLES)
        random.shuffle(self.deck)

    def deal_cards_before_game_start(self):
        self.shuffle_deck()
        for player in range(NUMBER_OF_PLAYERS):
            self.deal_cards_to_current_player(number_of_cards=3)
        for player in range(NUMBER_OF_PLAYERS):
            self.deal_cards_to_current_player(number_of_cards=2)
        """Deal first 5 cards to each player then execute announcement_phase method"""

        self.announcement_phase()
        if "ne vsichki sa PAS":
            for player in range(NUMBER_OF_PLAYERS):
                self.deal_cards_to_current_player(number_of_cards=3)
            """Deal last 3 card to each player if game is about to be played"""

    def deal_cards_to_current_player(self, number_of_cards=3):
        """Deal the desired number of cards to the player with the current index"""
        cards = []
        for _ in range(number_of_cards):
            cards.append(self.deal_single_card())
        self.PLAYER[self.current_player_idx].current_hand.extend(cards)
        self.change_current_player_index()

    def deal_single_card(self):
        top_card = self.deck.pop()  # removes the top card from the deck
        return top_card

    def change_current_player_index(self):
        """Rotate the index from 0 to 3 then 1 and again. This simulates the next player turn"""
        self.current_player_idx = self.current_player_idx + 1 if self.current_player_idx != 3 else 0

    def announcement_phase(self):
        """Here should be the logic of the announces that each player makes (VSICHKO KOZ KURVIII (zasega))"""
        self.announce = 'ALL_TRUMP'

    def compare_cards(self, card1, card2):
        """Simple compare for cards by color and power"""
        if list(COLORS).index(card1[1]) > list(COLORS).index(card2[1]):
            return True
        elif list(COLORS).index(card1[1]) == list(COLORS).index(card2[1]):
            if list(CARD_VALUE).index(card1[0]) > list(CARD_VALUE).index(card2[0]):
                return True
        return False

    def sort_hands(self, ):
        """Simple insertion sort for cards by color"""
        for x in range(NUMBER_OF_PLAYERS):
            tempHand = self.PLAYER[x].current_hand
            for y in range(1, len(tempHand)):
                key = tempHand[y]
                z = y - 1
                while z >= 0 and self.compare_cards(tempHand[z], key):
                    tempHand[z + 1] = tempHand[z]
                    z -= 1
                tempHand[z + 1] = key

    @staticmethod
    def search_by_color(hand, color):
        """Return True if the color is in the hand else False"""
        for idx in range(len(hand)):
            if hand[idx][1] == color:
                return True
        return False

    def play_card(self, card):
        """Logic about played card"""
        if not self.PLAYER[self.current_player_idx].current_hand:
            return False
        self.played_cards.append(card)
        self.PLAYER[self.current_player_idx].current_hand.remove(card)
        self.current_player_idx += 1
        if len(self.played_cards) == NUMBER_OF_PLAYERS:
            self.current_deal.append(self.played_cards)
            self.played_cards = []
            self.current_player_idx = 1
        return True

    def playable_cards(self, announce):
        """Logic about which cards are allowed to be played"""
        if not self.played_cards:
            return self.PLAYER[self.current_player_idx].current_hand
        if announce == "ALL_TRUMP":
            if not self.search_by_color(self.PLAYER[self.current_player_idx].current_hand, self.played_cards[0][1]):
                return self.PLAYER[self.current_player_idx].current_hand

            possible_options = []
            for x in self.PLAYER[self.current_player_idx].current_hand:
                if self.played_cards[0][1] == x[1]:
                    possible_options.append(x)
            if possible_options == []:
                return self.PLAYER[self.current_player_idx].current_hand
            else:
                return possible_options

    def playable_by_hand_and_played_cards(self, announce, hand, playedCards):
        """Logic about which cards are allowed to be played"""
        if not playedCards or playedCards == []:
            return hand

        if announce == "ALL_TRUMP":
            if not self.search_by_color(hand, playedCards[0][1]):
                return hand

            possible_options = []

            for x in hand:
                if playedCards[0][1] == x[1] and list(CARD_VALUE).index(x[0]) > list(CARD_VALUE).index(
                        playedCards[-1][0]):
                    possible_options.append(x)

            if possible_options == []:
                for x in hand:
                    if playedCards[0][1] == x[1]:
                        possible_options.append(x)

            if possible_options == []:
                return hand
            else:
                return possible_options

    def play_deals(self):
        """Logic about playing all possible deals with current hands"""
        self.sort_hands()
        temphands = [self.PLAYER[1].current_hand.copy(), self.PLAYER[2].current_hand.copy(),
                     self.PLAYER[3].current_hand.copy(), self.PLAYER[4].current_hand.copy()]
        already_in_counter = 0
        while already_in_counter < 100:
            playable_cards = self.playable_cards("ALL_TRUMP")
            while True:
                if not self.play_card(playable_cards[randbelow(len(playable_cards))]):
                    break
                playable_cards = self.playable_cards("ALL_TRUMP")
                if playable_cards == []:
                    break

            if self.current_deal in self.played_deals:
                already_in_counter += 1
                print("retard alg" + str(already_in_counter))
            else:
                self.played_deals.append(self.current_deal)
                already_in_counter = 0
                print("good alg" + str(len(self.played_deals)))
            self.current_deal = []

            for x in range(0, 4):
                self.PLAYER[x + 1].current_hand = temphands[x].copy()

        return len(self.played_deals)

    def play_recursive(self, turn_id, all_hands, played_cards, current_deal, first_cards=0, second_cards=0):
        """ TODO: Calculate possible moves
            TODO: Save played cards
            TODO: Optimise even more (numpy arrays)
        """
        if len(played_cards) == NUMBER_OF_PLAYERS:  # reset deal
            current_deal.append(played_cards)
            played_cards = []

        if first_cards != 0:  # turn reducing
            if turn_id == NUMBER_OF_PLAYERS * first_cards:
                self.first_deals_combinations.append(current_deal)  # save played game
                self.remaining_cards.append(all_hands)  # save remaining hands for the game
                self.return_when_all_cards_played()
                return True
        elif second_cards != 0:
            if turn_id == NUMBER_OF_PLAYERS * second_cards:
                self.return_when_all_cards_played()
                self.second_deal_combinations.append(current_deal)  # save played game
                return True
        elif turn_id == NUMBER_OF_CARDS:
            self.return_when_all_cards_played()
            return True

        current_player_idx = turn_id % NUMBER_OF_PLAYERS
        current_hand_copy = [*all_hands[current_player_idx]]

        self.change_current_player_index()
        for card in self.playable_by_hand_and_played_cards(self.announce, current_hand_copy,
                                                           played_cards):  # for each playable cards
            new_hand = [*current_hand_copy]
            new_hand.remove(card)
            new_played_cards = [*played_cards]
            new_played_cards.append(card)
            hands = [*all_hands]  # generate copies of new hands
            hands[current_player_idx] = new_hand
            self.play_recursive((turn_id + 1), [*hands], [*new_played_cards], [*current_deal], first_cards,
                                second_cards)  # play the next card

    def return_when_all_cards_played(self):
        self.played_deals_count += 1
        if self.played_deals_count % 5000000 == 0:
            print("finished" + str(self.played_deals_count))
        return True

    def play_deals_fast(self, first_cards=0, second_cards=0, deal_id=-1):
        """Logic about playing all possible deals with current hand"""
        self.sort_hands()
        temphands = [[*self.PLAYER[idx].current_hand] for idx in range(NUMBER_OF_PLAYERS)]
        if second_cards != 0:
            if deal_id == -1:
                for hand in temphands:
                    while len(hand) > second_cards:
                        del hand[0]  # removal of cards so there are second_cards left
            else:
                self.play_recursive(0, [self.remaining_cards[deal_id][idx] for idx in range(NUMBER_OF_PLAYERS)], [], [],
                                    first_cards, second_cards)
                return
        self.play_recursive(0, [temphands[idx] for idx in range(NUMBER_OF_PLAYERS)], [], [], first_cards, second_cards)

    def play_separated_to_x_then_y(self, cards):
        """ Dynamic programing alg for playing first all with x cards then all possible for them"""
        time_start = time.perf_counter()
        self.play_deals_fast(cards)  # play all combinations with first cards
        print("Played Deals with: " + str(cards) + ": " + str(len(self.first_deals_combinations)))

        for deal_id in range(len(self.first_deals_combinations)):  # for each of current played
            self.play_deals_fast(0, HAND_SIZE - cards, deal_id)  # play all combinations with last cards
            time_write = time.perf_counter()  # time for writing start
            for idx in range(len(self.second_deal_combinations)):
                combined_deals = self.first_deals_combinations[deal_id] + self.second_deal_combinations[idx]
                # append to each played first cards the last played cards
                self.played_deals.append(combined_deals)
            self.second_deal_combinations = []  # reset played second cards
            time_write = time.perf_counter() - time_write  # calc time write
            print(time_write)
            timeEnd = time.perf_counter() - time_start  # current time for calculating
            print("Current Played: " + str(len(self.played_deals)) + " time:" + str(timeEnd))


if __name__ == '__main__':
    g = Game([HumanPlayer(), HumanPlayer(), HumanPlayer(), HumanPlayer()])
    g.deal_cards_before_game_start()
    for i in range(NUMBER_OF_PLAYERS):
        print(g.PLAYER[i].current_hand)
    g.play_separated_to_x_then_y(3)