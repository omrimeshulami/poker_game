from Deck import Deck
import random
from Enums import Status
import threading
from Player import Player
import functools
import numpy as np
from collections import defaultdict

lock = threading.Lock()


class Table:
    def __init__(self, small_blind_value, big_blind_value, starting_cash):
        self.pot = 0
        self.players = {}
        self.players_remaining = []
        self.small_blind_player = ""  #
        self.big_blind_player = ""
        self.dealer_button_player = ""
        self.small_blind_value = small_blind_value
        self.big_blind_value = big_blind_value
        self.deck = Deck()
        self.cards_on_the_table = []
        self.player_who_started_the_round = ""
        self.current_player = ""
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
            self.players_remaining.remove(name)
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
        player = Player(name, self.starting_cash)
        self.players[name] = player
        lock.release()

    def init_table(self):
        self.new_mini_game()
        self.run_game()

    def run_game(self):
        while len(self.players_remaining) > 1 and not self.is_mini_game_over():
            action = input(
                f'{self.current_player} turn:\n Hand:{self.players[self.current_player].hand.print_hand()}  Enter your action:Actions:\nFOLD: fold\nCALL: call\nRAISE: raise 100\n')
            self.player_action(action, self.current_player)

    def open_new_card(self):
        if len(self.cards_on_the_table) == 0:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_flop()))
        elif len(self.cards_on_the_table) == 3:
            self.cards_on_the_table.append(self.deck.the_turn())
        else:
            self.cards_on_the_table.append(self.deck.the_river())

    # TODO FINISHED
    def collect_blinds(self):
        self.players[self.small_blind_player].bank_account.call(self.small_blind_value)
        self.pot += self.small_blind_value
        self.pot += self.players[self.big_blind_player].bank_account.call(self.big_blind_value)
        self.pot += self.big_blind_value

    # TODO FINISHED
    def update_players_bank_after_mini_game(self, name):
        for p in self.players:
            p.bank_accout.fold()
        self.players[name].back_account.won_mini_game_update(self.pot)

    # list(players.keys())[0]    ket first key

    def winner(self):
        text = ""
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
        # TODO will need to add the case if there are two peple with same hand power with the same invest
        for key in group_by_invest.keys():
            max = functools.reduce(lambda a, b: a if a.hand_rank > b.hand_rank else b, group_by_invest[key])
            for i in key:
                if key[i]['hand_rank'] != max:
                    key.pop(i)
        players_to_choose_from = []
        for key in group_by_invest.keys():
            players_to_choose_from = np.concatenate((players_to_choose_from, group_by_invest[key]))

        player_ordered_by_rank = players_to_choose_from.sort(key=lambda x: x['hand_rank'], reverse=True)
        player_ordered_by_invest = players_to_choose_from.sort(key=lambda x: x['money_invest'], reverse=True)
        invest_counts = defaultdict(lambda: 0)
        for p in players_to_choose_from:
            invest_counts[p['money_invest']] += 1
        hand_rank_counts = defaultdict(lambda: 0)
        for p in players_to_choose_from:
            hand_rank_counts[p['hand_rank']] += 1
        while players_to_choose_from != []:
            player_to_check = player_ordered_by_rank[0]
            pot_for_the_winner = 0
            if hand_rank_counts[player_to_check['hand_rank']] == 1:
                for p in self.players:
                    if p.bank_accout.mini_game_invest <= player_to_check['money_invest']:
                        pot_for_the_winner += p.bank_accout.mini_game_invest
                        if player_ordered_by_rank.contained(p):
                            player_ordered_by_invest.remove(p)  # TODO 100% wrong syntax
                            player_ordered_by_rank.remoce(p)  # TODO 100% wrong syntax
                        p.bank_accout.fold()
                self.players[player_to_check['name']].bank_account.won_mini_game_update(pot_for_the_winner)
                text += "the name of the player , hand rank and pot"

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
        for p in self.players.keys():
            print(p)
            if self.players[p].bank_account.total_cash > 0:
                self.players_remaining.append(self.players[p].name)
        self.deck = Deck()
        self.pot = 0
        if self.small_blind_player == "":
            self.init_buttons()
        else:
            self.update_buttons()
        self.deck.deal_cards(self.players)
        self.collect_blinds()
        self.table_status()

    # TODO FINISHED
    def end_mini_game(self):
        winner = self.winner()
        self.update_players_bank_after_mini_game(winner)
        self.new_mini_game()

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
        players_cash = ""
        text += f'Pot: {self.pot}\n'
        text += f'Dealer Button: {self.dealer_button_player}\n'
        text += f'Small blind: {self.small_blind_player}\n'
        text += f'Big blind:: {self.big_blind_player}\n'
        for key in self.players.keys():
            players_cash += f'{self.players[key].name}:\tCash:{self.players[key].bank_account.max_bet},\tStatus:{self.players[key].status}\n'
        text += players_cash
        print(text)

    ################ GETTERS ###################
    # TODO FINISHED
    def get_player_hand(self, name):
        return self.players[name].hand

    ############## BUTTON METHODS ##############
    # TODO FINISHED
    def init_buttons(self):
        random.shuffle(self.players_remaining)
        if len(self.players_remaining) == 2:
            self.small_blind_player = self.players_remaining[0]
            self.big_blind_player = self.players_remaining[1]
            self.player_who_started_the_round = self.players_remaining[0]
            self.current_player = self.players_remaining[0]

        else:
            self.dealer_button_player = self.players_remaining[0]
            self.small_blind_player = self.players_remaining[1]
            self.big_blind_player = self.players_remaining[2]
            self.player_who_started_the_round = self.players_remaining[0]
            self.current_player = self.players_remaining[0]

    # TODO FINISHED
    def update_buttons(self):
        if len(self.players_remaining) == 2:
            if self.small_blind_player != self.players_remaining[0]:
                self.small_blind_player = self.players_remaining[0]
                self.big_blind_player = self.players_remaining[1]
                self.current_player = self.players_remaining[0]
                self.player_who_started_the_round = self.players_remaining[0]

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
            self.player_who_started_the_round = self.players_remaining[
                self.players_remaining.index(self.dealer_button_player) + 1 % len(self.players)]
