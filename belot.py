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
        self.playOnlyFirstCards = 0 # for test
        self.playOnlyLastCards = 0 # for test

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

    def sort_hands(self):
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

    def play_recursive(self, turn_id, all_hands, played_cards, current_deal):
        """ TODO: Calculate possible moves;
            TODO: Save played cards
            TODO: Optimise even more (numpy arrays)
        """
        if self.playOnlyFirstCards != 0: # turn reducing
            if turn_id == NUMBER_OF_PLAYERS * self.playOnlyFirstCards:
                self.return_when_all_cards_played()
                return True
        elif self.playOnlyLastCards != 0:
            if turn_id == NUMBER_OF_PLAYERS * self.playOnlyLastCards:
                self.return_when_all_cards_played()
                return True
        elif turn_id == NUMBER_OF_CARDS:
            self.return_when_all_cards_played()
            return True

        current_player_idx = turn_id % NUMBER_OF_PLAYERS
        current_hand_copy = [*all_hands[current_player_idx]]

        if len(played_cards) == NUMBER_OF_PLAYERS:
            current_deal.append(played_cards)
            played_cards = []

        self.change_current_player_index()
        for card in self.playable_by_hand_and_played_cards(self.announce, current_hand_copy, played_cards):
            new_hand = [*current_hand_copy]
            new_hand.remove(card)
            new_played_cards = [*played_cards]
            new_played_cards.append(card)
            hands = [*all_hands]
            hands[current_player_idx] = new_hand
            self.play_recursive((turn_id + 1), hands, [*new_played_cards], [*current_deal])

    def return_when_all_cards_played(self):
        self.played_deals_count += 1
        if self.played_deals_count % 5000000 == 0:
            print("finished" + str(self.played_deals_count))
        return True

    def play_deals_fast(self):
        """Logic about playing all possible deals with current hands"""
        self.sort_hands()                
        temphands = [self.PLAYER[idx].current_hand.copy() for idx in range(NUMBER_OF_PLAYERS)]
        if self.playOnlyLastCards != 0:
            for hand in temphands:
                while len(hand) > self.playOnlyLastCards:
                    hand.pop() # removal of cards so there are 5 left

        self.play_recursive(0, [temphands[idx] for idx in range(NUMBER_OF_PLAYERS)], [], [])
        if self.playOnlyFirstCards != 0:
            print("Played Deals with only first" + str(self.playOnlyFirstCards) + " cards: " + str(self.played_deals_count))
        elif self.playOnlyLastCards != 0:
            print("Played Deals with only random last" +  str(self.playOnlyLastCards) + " cards: " + str(self.played_deals_count))  
        else:
            print(self.played_deals_count)


if __name__ == '__main__':
    g = Game([HumanPlayer(), HumanPlayer(), HumanPlayer(), HumanPlayer()])
    g.deal_cards_before_game_start()
    for i in range(NUMBER_OF_PLAYERS):
        print(g.PLAYER[i].current_hand)
    g.playOnlyFirstCards = 2 # check how many are first 2 cards combinations and how fast are they played
    timeStart = time.perf_counter()
    g.play_deals_fast()
    timeEnd = time.perf_counter() - timeStart
    print("time for first" +  str(g.playOnlyFirstCards) + " cards :" + str(timeEnd))

    h = Game([HumanPlayer(), HumanPlayer(), HumanPlayer(), HumanPlayer()])
    h.deal_cards_before_game_start()
    for i in range(NUMBER_OF_PLAYERS):
        print(h.PLAYER[i].current_hand)
    h.playOnlyLastCards = 6 # check how many are last 6 cards combinations and how fast are they played
    timeStart2 = time.perf_counter()
    h.play_deals_fast()
    timeEnd2 = time.perf_counter() - timeStart2
    print("time for last" + str(h.playOnlyLastCards)+ " cards : " + str(timeEnd2))

    print("Total estimated combs with " + str(g.playOnlyFirstCards) + " * " + str(h.playOnlyLastCards) + ": " + str(h.played_deals_count * g.played_deals_count)) 
    print(" Potential time for first idea: " + str((timeEnd + h.played_deals_count * timeEnd2) / 3600) + " hours" )

    a = Game([HumanPlayer(), HumanPlayer(), HumanPlayer(), HumanPlayer()])
    a.deal_cards_before_game_start()
    for i in range(NUMBER_OF_PLAYERS):
        print(a.PLAYER[i].current_hand)
    a.playOnlyFirstCards = 3 # check how many are first 3 cards combinations and how fast are they played
    timeStart = time.perf_counter()
    a.play_deals_fast()
    timeEnd = time.perf_counter() - timeStart
    print("time for first" +  str(a.playOnlyFirstCards) + " cards :" + str(timeEnd))

    b = Game([HumanPlayer(), HumanPlayer(), HumanPlayer(), HumanPlayer()])
    b.deal_cards_before_game_start()
    for i in range(NUMBER_OF_PLAYERS):
        print(b.PLAYER[i].current_hand)
    b.playOnlyLastCards = 5 # check how many are last 5 cards combinations and how fast are they played
    timeStart2 = time.perf_counter()
    b.play_deals_fast()
    timeEnd2 = time.perf_counter() - timeStart2
    print("time for last" + str(b.playOnlyLastCards)+ " cards : " + str(timeEnd2))

    print("Total estimated combs with " + str(a.playOnlyFirstCards) + " * " + str(b.playOnlyLastCards) + ": " + str(b.played_deals_count * a.played_deals_count)) 
    print(" Potential time for first idea: " + str((timeEnd + b.played_deals_count * timeEnd2) / 3600) + " hours" )

