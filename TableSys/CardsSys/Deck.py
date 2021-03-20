from .Card import Card
from Enums import Symbol
import random


class Deck:
    def __init__(self):
        self.deck = self.shuffle()

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
        self.deck = self.deck[:-2]
        return card_to_reveal

    def deal_cards(self, players):
        for key in players:
            players[key].hand.first = self.deck[len(self.deck) - 1]  # DEAL ONE CARD TO EACH PLAYER
            self.deck = self.deck[:-1]

        for key in players:
            players[key].hand.second = self.deck[len(self.deck) - 1]  # DEAL ONE CARD TO EACH PLAYER
            self.deck = self.deck[:-1]

    # TODO check if work
    def shuffle(self):
        deck1 = [Card(number, symbol) for number in range(2, 15) for symbol in list(map(lambda c: c.value, Symbol))]
        deck = []
        for i in range(2, 15):
            deck.append(Card(i, Symbol.HEARTS.value))
            deck.append(Card(i, Symbol.SPADES.value))
            deck.append(Card(i, Symbol.CLUBS.value))
            deck.append(Card(i, Symbol.DIAMONDS.value))

        random.shuffle(deck)
        return deck
