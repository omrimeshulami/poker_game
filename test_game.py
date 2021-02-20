from Table import Table
from PlayerHand import PlayerHand
from Enums import CardValue, Symbol
from Card import Card
from Deck import Deck
import numpy as np
from Player import Player

# GAME SETTING
STARTING_CASH = 1000
MINIMUM_NUMBER_OF_PLAYERS = 2
MAXIMUM_NUMBER_OF_PLAYERS = 5
SMALL_BLIND_VALUE = 5
BIG_BLIND_VALUE = 10

# GAME CONFIGURATION


if __name__ == '__main__':
    table = Table(SMALL_BLIND_VALUE, BIG_BLIND_VALUE, STARTING_CASH)
    names = ['Player1', 'Player2', 'Player3']
    player = Player('name', 1000)
    for i in range(0, len(names)):
        table.register_player(names[i])
    table.init_table()


    # hand = PlayerHand()
    # for i in range(1, 10000):
    #     deck = Deck()
    #     hand.first = deck.the_turn()
    #     hand.second = deck.the_turn()
    #     table_cards = np.concatenate(([deck.the_turn(), deck.the_river()], deck.the_flop()))
    #     other_three_cards = []
    #     table_values = []
    #     for c in table_cards:
    #         table_values.append(c.value)
    #     table_symbol = []
    #     for c in table_cards:
    #         table_symbol.append(c.symbol)
    #     print(f"Hand: ({hand.first.value},{hand.first.symbol}), ({hand.second.value},{hand.second.symbol}) \n")
    #     print(f"Card On The Table: {table_values}, {table_symbol} \n")
    #     print(f"Best Hand Rank is: {hand.calculate_strength(table_cards)}")
