import Deck
import random


class Table:
    def __init__(self, players, small_blind_value, big_blind_value):
        self.pot = 0
        self.players = players
        self.small_blind_player = {'name': '', 'index': None}
        self.big_blind_player = {'name': '', 'index': None}
        self.dealer_button_player = {'name': '', 'index': None}
        self.small_blind_value = small_blind_value
        self.big_blind_value = big_blind_value
        self.deck = Deck.Deck()
        self.init_buttons()
        self.collect_blinds()

    def new_round(self):
        self.deck = Deck.Deck()
        self.pot = 0

    def table_status(self):
        text = ''
        text += f'Pot: {self.pot}\n'
        text += f'dealerB: {self.dealer_button_player.name}\n'
        text += f'big blind: {self.dealer_button_player.name}\n'
        text += f'small blind:: {self.dealer_button_player.name}\n'
        for player in enumerate(self.players):
            players_cash = f'{player.name}:\t\t{player.bank.max_bet}\n'
        text += players_cash
        return

    def get_player_hand(self, name):
        for player in self.players:
            if (player.name == name):
                return player.hand
    def collect_blinds(self):
        self.players[self.small_blind_player].bank.call(5)

    def init_buttons(self):
        random.shuffle(self.players)
        if len(self.players) == 2:
            self.small_blind_player.name = self.players[0].name
            self.small_blind_player.index = self.players[0].index
            self.big_blind_player.name = self.players[1].name
            self.big_blind_player.index = self.players[1].index

        else:
            self.dealer_button_player.name = self.players[0].name
            self.dealer_button_player.index = self.players[0].index
            self.small_blind_player.name = self.players[1].name
            self.small_blind_player.index = self.players[1].index
            self.big_blind_player.name = self.players[2].name
            self.big_blind_player.index = self.players[2].index

    def update_buttons(self):
        if len(self.players) == 2:
            if self.small_blind_player.index != 0:
                self.small_blind_player.name = self.players[0].name
                self.small_blind_player.index = self.players[0].index
                self.big_blind_player.name = self.players[1].name
                self.big_blind_player.index = self.players[1].index
        else:
            # if we have enough room to move the buttons
            if self.dealer_button_player.index + 3 <= len(self.players) - 1:
                self.dealer_button_player.name = self.players[self.dealer_button_player.index + 1].name
                self.dealer_button_player.index = self.players[self.dealer_button_player.index + 1].index
                self.small_blind_player.name = self.players[self.dealer_button_player.index + 1].name
                self.small_blind_player.index = self.players[self.dealer_button_player.index + 1].index
                self.big_blind_player.name = self.players[self.dealer_button_player.index + 1].name
                self.big_blind_player.index = self.players[self.dealer_button_player.index + 1].index

            # if we missing 1 space in the array move the buttons
            if self.dealer_button_player.index + 2 == len(self.players) - 1:
                self.dealer_button_player.name = self.players[self.dealer_button_player.index + 1].name
                self.dealer_button_player.index = self.players[self.dealer_button_player.index + 1].index
                self.small_blind_player.name = self.players[self.dealer_button_player.index + 1].name
                self.small_blind_player.index = self.players[self.dealer_button_player.index + 1].index
                self.big_blind_player.name = self.players[0].name
                self.big_blind_player.index = self.players[0].index

            # if we missing 1 space in the array move the buttons
            if self.dealer_button_player.index + 1 == len(self.players) - 1:
                self.dealer_button_player.name = self.players[self.dealer_button_player.index + 1].name
                self.dealer_button_player.index = self.players[self.dealer_button_player.index + 1].index
                self.small_blind_player.name = self.players[0].name
                self.small_blind_player.index = self.players[0].index
                self.big_blind_player.name = self.players[1].name
                self.big_blind_player.index = self.players[1].index

            # if we missing 0 space in the array move the buttons
            if self.dealer_button_player.index == len(self.players) - 1:
                self.dealer_button_player.name = self.players[0].name
                self.dealer_button_player.index = self.players[0].index
                self.small_blind_player.name = self.players[1].name
                self.small_blind_player.index = self.players[1].index
                self.big_blind_player.name = self.players[2].name
                self.big_blind_player.index = self.players[2].index
