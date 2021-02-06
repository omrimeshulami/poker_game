import Deck
import random
from Enums import Status


# TODO pot system,compare same lvl of hands,action player raised

class Table:
    def __init__(self, players, small_blind_value, big_blind_value):
        self.pot = 0  # TODO maybe create class for pot to manage the pot/side pot and who wins what
        self.players = players
        self.players_remaining = [p.name for p in players]
        self.small_blind_player = None  #
        self.big_blind_player = None
        self.dealer_button_player = None
        self.small_blind_value = small_blind_value
        self.big_blind_value = big_blind_value
        self.deck = Deck.Deck()
        self.init_buttons()
        self.collect_blinds()
        self.cards_on_the_table = []
        self.player_turn_start = None
        self.current_player = self.dealer_button_player

    '''
    Actions:
    FOLD: "fold"
    CALL: "call"
    RAISE: "raise 100"
     '''

    def is_round_over(self):
        for p in self.players_remaining:
            if p.status == Status.RAISED:
                return False
        return True

    def is_mini_game_over(self):
        if len(self.cards_on_the_table) != 5:
            return False
        for p in self.players_remaining:
            if p.status == Status.RAISED:
                return False
        return True

    def new_round(self):
        self.open_new_card()
        # TODO will need to update pot object and
        for p in self.players_remaining:
            self.players[p].back_account.new_round()

    def switch_to_next_player(self):
        if self.players_remaining.index(self.current_player) + 1 <= len(self.players_remaining) - 1:
            self.current_player = self.players_remaining[
                self.players_remaining.index(self.current_player) + 1]
        else:
            self.current_player = self.players_remaining[0]

    def player_action(self, action, name):
        actions_parts = action.split()
        if actions_parts[0].lower() == "fold":
            self.players[name].status = Status.FOLDED
            self.players_remaining.pop(name)
            self.players[name].bank_account.fold()  # TODO need update pot after create pot system
            if not self.is_round_over():
                self.switch_to_next_player()
            elif self.is_mini_game_over():
                self.new_mini_game()
            else:
                self.new_round()
            return

        elif actions_parts[0].lower() == "call":
            self.players[name].status = Status.CALLED
            self.players[name].bank_account.call()  # TODO need update pot after create pot system
            if not self.is_round_over():
                self.switch_to_next_player()
            elif self.is_mini_game_over():
                self.new_mini_game()
            else:
                self.new_round()
            return

    def open_new_card(self):
        if len(self.cards_on_the_table) == 0:
            self.cards_on_the_table.append(self.deck.the_flop())
        elif len(self.cards_on_the_table) == 3:
            self.cards_on_the_table.append(self.deck.the_turn())
        else:
            self.cards_on_the_table.append(self.deck.the_river())

    def winner_name(self):
        pass

    def new_mini_game(self):
        self.deck = Deck.Deck()
        self.pot = 0
        self.update_buttons()

    def table_status(self):
        text = ''
        text += f'Pot: {self.pot}\n'
        text += f'Dealer Button: {self.dealer_button_player}\n'
        text += f'Small blind: {self.small_blind_player}\n'
        text += f'Big blind:: {self.big_blind_player}\n'
        for player in enumerate(self.players):
            players_cash = f'{player.name}:\t\t{player.bank.max_bet}\n'
        text += players_cash
        return

    def get_player_hand(self, name):
        return self.players[name].hand

    def collect_blinds(self):
        self.players[self.small_blind_player].bank.call(self.small_blind_value)
        self.players[self.big_blind_player].bank.call(self.big_blind_value)

    def init_buttons(self):
        random.shuffle(self.players)
        if len(self.players_remaining) == 2:
            self.small_blind_player = self.players[0]
            self.big_blind_player = self.players[1]
            self.player_turn_start = self.players[0]

        else:
            self.dealer_button_player = self.players[0]
            self.small_blind_player = self.players[1]
            self.big_blind_player = self.players[2]
            self.player_turn_start = self.players[0]

    def update_buttons(self):
        if len(self.players_remaining) == 2:
            if self.small_blind_player != self.players_remaining[0]:
                self.small_blind_player = self.players_remaining[0]
                self.big_blind_player = self.players_remaining[1]
        else:
            # if we have enough room to move the buttons
            if self.players_remaining.index(self.dealer_button_player) + 3 <= len(self.players_remaining) - 1:
                self.dealer_button_player = self.players_remaining[
                    self.players_remaining.index(self.dealer_button_player) + 1]
                self.small_blind_player = self.players_remaining[
                    self.players_remaining.index(self.dealer_button_player) + 2]
                self.big_blind_player = self.players_remaining[
                    self.players_remaining.index(self.dealer_button_player) + 3]

            # if we missing 1 space in the array move the buttons
            if self.players_remaining.index(self.dealer_button_player) + 2 <= len(self.players_remaining) - 1:
                self.dealer_button_player = self.players_remaining[
                    self.players_remaining.index(self.dealer_button_player) + 1]
                self.small_blind_player = self.players_remaining[
                    self.players_remaining.index(self.dealer_button_player) + 2]
                self.big_blind_player = self.players_remaining[0]

            # if we missing 2 space in the array move the buttons
            if self.players_remaining.index(self.dealer_button_player) + 1 <= len(self.players_remaining) - 1:
                self.dealer_button_player = self.players_remaining[
                    self.players_remaining.index(self.dealer_button_player) + 1]
                self.small_blind_player = self.players_remaining[0]
                self.big_blind_player = self.players_remaining[1]

            # if we missing 3 space in the array move the buttons
            if self.players_remaining.index(self.dealer_button_player) <= len(self.players_remaining) - 1:
                self.dealer_button_player = self.players_remaining[0]
                self.small_blind_player = self.players_remaining[1]
                self.big_blind_player = self.players_remaining[2]
