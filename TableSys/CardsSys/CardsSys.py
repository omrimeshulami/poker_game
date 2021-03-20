import numpy as np

from TableSys.CardsSys.Deck import Deck


class CardSystem:
    def __init__(self):
        self.deck = Deck()
        self.cards_on_the_table = []

    def open_rest_of_cards(self):
        if len(self.cards_on_the_table) == 0:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_flop()))
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_turn()))
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))
        elif len(self.cards_on_the_table) == 3:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_turn()))
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))
        elif len(self.cards_on_the_table) == 4:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))


    def open_new_card(self):
        if len(self.cards_on_the_table) == 0:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_flop()))
        elif len(self.cards_on_the_table) == 3:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_turn()))
        elif len(self.cards_on_the_table) == 4:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))
