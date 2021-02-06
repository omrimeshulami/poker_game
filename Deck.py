from Card import Card
from Enums import Symbol
import random
import Player


class Deck:
    def __init__(self):
        self.deck = []
        for i in range(1, 15):
            self.deck.append(Card(i, Symbol.HEARTS))
            self.deck.append(Card(i, Symbol.SPADES))
            self.deck.append(Card(i, Symbol.CLUBS))
            self.deck.append(Card(i, Symbol.DIAMONDS))

        random.shuffle(self.deck)

    def the_flop(self):
        card_to_reveal = self.deck[-3:]
        self.deck = self.deck[:-4]
        return card_to_reveal

    def the_turn(self):
        card_to_reveal = self.deck[-1:]
        self.deck = self.deck[:-2]
        return card_to_reveal

    def the_river(self):
        card_to_reveal = self.deck[-1:]
        return card_to_reveal

    def deal_cards(self, players):
        for i in range(0, len(players)):
            players[i].hand.first = self.deck[len(self.deck) - 1:]  # DEAL ONE CARD TO EACH PLAYER
            self.deck = self.deck[:-1]

        for i in range(0, len(players)):
            players[i].hand.second = self.deck[len(self.deck) - 1:]  # DEAL ONE CARD TO EACH PLAYER
            self.deck = self.deck[:-1]

    def new_mini_game(self):
        self.deck = []
        for i in range(1, 15):
            self.deck.append(Card(i, Symbol.HEARTS))
            self.deck.append(Card(i, Symbol.SPADES))
            self.deck.append(Card(i, Symbol.CLUBS))
            self.deck.append(Card(i, Symbol.DIAMONDS))

        random.shuffle(self.deck)
