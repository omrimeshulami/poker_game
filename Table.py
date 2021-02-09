import Deck
import random
from Enums import Status
import threading
import Player
import functools

lock = threading.Lock()



class Table:
    def __init__(self, small_blind_value, big_blind_value, starting_cash):
        self.pot = 0
        self.players = {}
        self.players_remaining = []
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
        self.starting_cash = starting_cash

    '''
    Actions:
    FOLD: "fold"
    CALL: "call"
    RAISE: "raise 100"
     '''

    def player_action(self, action, name):
        actions_parts = action.split()
        if actions_parts[0].lower() == "fold":
            self.players[name].status = Status.FOLDED  # TODO "FOLD" LOOKS LIKE ITS FINISHED
            self.players_remaining.pop(name)
            self.players[name].bank_account.fold()
            if len(self.players_remaining) == 1:
                self.end_mini_game()
            else:
                self.complete_player_turn()

        elif actions_parts[0].lower() == "call":  # TODO "CALL" LOOKS LIKE ITS FINISHED
            max_raise_yet = 0
            self.players[name].status = Status.CALLED
            for p in self.players:
                if p.bank_accout.round_invested > max_raise_yet:
                    max_raise_yet = p.bank_accout.round_invested
            if self.players[name].bank_account.need_all_in(max_raise_yet):
                self.players[name].staus = Status.ALL_IN
            self.players[name].bank_account.call(max_raise_yet)
            self.complete_player_turn()
            return
        elif actions_parts[0].lower() == "raise":
            self.players[name].status = Status.RAISED  # TODO "FOLD" LOOKS LIKE ITS FINISHED
            self.players[name].bank_account.raise_bet(actions_parts[1])
            self.pot += int(actions_parts[1])

    def complete_player_turn(self):
        if not self.is_round_over():
            self.switch_to_next_player()
        elif self.is_mini_game_over():
            self.new_mini_game()
        else:
            self.new_round()
        return

    ############## TABLE METHODS #################
    def register_player(self, name):
        lock.acquire()
        self.players[name] = Player(name, self.starting_cash)
        self.players_remaining.append(name)
        lock.release()

    # TODO FINISHED
    def open_new_card(self):
        if len(self.cards_on_the_table) == 0:
            self.cards_on_the_table.append(self.deck.the_flop())
        elif len(self.cards_on_the_table) == 3:
            self.cards_on_the_table.append(self.deck.the_turn())
        else:
            self.cards_on_the_table.append(self.deck.the_river())

    # TODO FINISHED
    def collect_blinds(self):
        self.players[self.small_blind_player].bank.call(self.small_blind_value)
        self.players[self.big_blind_player].bank.call(self.big_blind_value)

    # TODO FINISHED
    def update_players_bank_after_mini_game(self, name):
        for p in self.players:
            p.bank_accout.fold()
        self.players[name].back_account.won_mini_game_update(self.pot)

    # list(players.keys())[0]    ket first key

    def winner(self):
        players_to_choose_from = []
        for p in self.players:
            if p.status != Status.FOLDED and p.status != Status.WAIT_FOR_TURN:
                players_to_choose_from.append(p)

        group_by_invest = {}
        for p in players_to_choose_from:  # seet the dict with key of iveste and empy array
            group_by_invest[p.bank_accout.mini_game_invest] = []
        for p in players_to_choose_from:  # inest values to the array
            group_by_invest[str(p.bank_accout.mini_game_invest)].append(
                {'name': p.name, 'hand_rank': p.hand.calculate_strength(self.cards_on_the_table),
                 'money_invest': p.bank_accout.mini_game_invest})

        for key in group_by_invest.keys():
            functools.reduce(lambda a, b: a if a.hand_rank > b.hand_rank else b, group_by_invest[key])
        players_to_choose_from = []
        for key in group_by_invest.keys():
            players_to_choose_from.append(group_by_invest[key][0])

        players_to_choose_from.sort(key=lambda x: x['hand_rank'], reverse=True)
        # TODO i have until here array of the groups winners ordered by hand rank

    # TODO FINISHED
    def switch_to_next_player(self):
        while True:
            self.current_player = self.players_remaining[
                self.players_remaining.index(self.current_player) + 1 % len(self.players_remaining)]
            if self.players[self.current_player].status != Status.ALL_IN:
                return

    ############# ROUND METHODS ###################
    # TODO FINISHED
    def new_round(self):
        self.open_new_card()
        for p in self.players:
            p.status = Status.WAIT_FOR_TURN

    # TODO FINISHED
    def end_round(self):
        for p in self.players:
            self.pot += p.back_account.round_invested
            self.p.back_account.new_round()

    # the idea check if every one in the table is check or everyone is check and the next player is rasied
    # TODO FINISHED
    def is_round_over(self):
        next_player_name = self.players_remaining[
            self.players_remaining.index(self.current_player) + 1]
        if self.players[next_player_name].status == Status.RAISED:
            for n in self.players_remaining:
                if self.players[n].status != Status.CALLED and n != next_player_name:
                    return False
        for n in self.players_remaining:
            if self.players[n].status != Status.CHECKED:
                return False
        return True

    # TODO FINISHED
    ########### MINI GAME METHODS ###############
    def new_mini_game(self):
        self.deck = Deck.Deck()
        self.pot = 0
        self.update_buttons()

    # TODO FINISHED
    def end_mini_game(self):
        winner = self.winner()
        self.update_players_bank_after_mini_game(winner)

    # TODO FINISHED
    def is_mini_game_over(self):
        if len(self.cards_on_the_table) == 5 and self.is_round_over():
            return True
        else:
            return False

    ############# PRINT METHODS #################
    # TODO FINISHED
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

    ################ GETTERS ###################
    # TODO FINISHED
    def get_player_hand(self, name):
        return self.players[name].hand

    ############## BUTTON METHODS ##############
    # TODO FINISHED
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

    # TODO FINISHED
    def update_buttons(self):
        if len(self.players_remaining) == 2:
            if self.small_blind_player != self.players_remaining[0]:
                self.small_blind_player = self.players_remaining[0]
                self.big_blind_player = self.players_remaining[1]
                self.current_player = self.players_remaining[0]
        else:
            # if we have enough room to move the buttons
            self.dealer_button_player = self.players_remaining[
                self.players_remaining.index(self.dealer_button_player) + 1 % len(self.players)]
            self.small_blind_player = self.players_remaining[
                self.players_remaining.index(self.small_blind_player) + 1 % len(self.players)]
            self.big_blind_player = self.players_remaining[
                self.players_remaining.index(self.big_blind_player) + 1 % len(self.players)]
            self.current_player = self.players_remaining[
                self.players_remaining.index(self.dealer_button_player) + 1 % len(self.players)]
