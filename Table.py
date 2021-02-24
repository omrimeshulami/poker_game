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
        self.is_last_player_folded = False
        self.folded_player_index = None

    '''
    Actions:
    FOLD: "fold"
    CALL: "call"
    RAISE: "raise 100"
     '''

    def player_action(self, action):
        someone_raised = False
        for key in self.players.keys():
            if self.players[key].status == Status.RAISED.value:
                someone_raised = True
        actions_parts = action.split()
        if actions_parts[0].lower() == "check" and someone_raised == False:
            self.is_last_player_folded = False
            self.folded_player_index = 0
            self.complete_player_turn_and_switch_player()
        if actions_parts[0].lower() == "fold":
            self.is_last_player_folded = True
            self.folded_player_index = self.players_remaining.index(self.current_player)
            self.players[self.current_player].status = Status.FOLDED.value  # TODO "FOLD" LOOKS LIKE ITS FINISHED
            self.players_remaining.remove(self.current_player)
            if len(self.players_remaining) == 1:
                self.end_mini_game()
                return True
            else:
                self.complete_player_turn_and_switch_player()
                return True

        elif actions_parts[0].lower() == "call":  # TODO "CALL" LOOKS LIKE ITS FINISHED
            max_raise_yet = 0
            self.players[self.current_player].status = Status.CALLED.value
            for name in self.players_remaining:
                if self.players[name].bank_account.round_invested > max_raise_yet:
                    max_raise_yet = self.players[name].bank_account.round_invested
                    print(max_raise_yet)
            if self.players[self.current_player].bank_account.need_all_in(max_raise_yet):
                self.players[self.current_player].staus = Status.ALL_IN.value
            self.pot += max_raise_yet - self.players[self.current_player].bank_account.round_invested
            self.players[self.current_player].bank_account.call(
                max_raise_yet - self.players[self.current_player].bank_account.round_invested)
            self.is_last_player_folded = False
            self.folded_player_index = 0
            self.complete_player_turn_and_switch_player()
            return True
        elif actions_parts[0].lower() == "raise" and len(actions_parts) == 2 and actions_parts[1].isnumeric():
            self.players[self.current_player].status = Status.RAISED.value  # TODO "FOLD" LOOKS LIKE ITS FINISHED
            self.players[self.current_player].bank_account.raise_bet(actions_parts[1])
            self.pot += int(actions_parts[1])
            self.is_last_player_folded = False
            self.folded_player_index = 0
            self.complete_player_turn_and_switch_player()
            return True
        return False

    def complete_player_turn_and_switch_player(self):
        print(f'the value of mini game is:{self.is_mini_game_over()}')
        print(f'the value of round is:{self.is_round_over()}')

        if self.is_mini_game_over():
            self.end_mini_game()
        elif self.is_round_over():
            self.new_round()

        self.switch_to_next_player()
        return

    ############## TABLE METHODS #################
    def register_player(self, name):
        lock.acquire()
        player = Player(name, self.starting_cash)
        self.players[name] = player
        lock.release()

    def init_table(self):
        self.new_mini_game()

    def run_game(self):
        while not self.is_mini_game_over():
            self.table_status()
            someone_raised = False
            for key in self.players.keys():
                if self.players[key].status == Status.RAISED.value:
                    someone_raised = True
            check_option = "CHECK: check\n"
            action = input(
                f'{self.current_player} turn:\n Hand:{self.players[self.current_player].hand.print_hand()}\nEnter your action:\nActions:\n{check_option if not someone_raised else ""}FOLD: fold\nCALL: call\nRAISE: raise 100\n')
            if self.player_action(action) == False:
                print(f'ILLIGAL ACTION PLEASE TRY AGAIN')
        self.end_mini_game()

    def open_new_card(self):
        if len(self.cards_on_the_table) == 0:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_flop()))
        elif len(self.cards_on_the_table) == 3:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_turn()))
        else:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))

    # TODO FINISHED
    def collect_blinds(self):
        self.players[self.small_blind_player].bank_account.call(self.small_blind_value)
        self.pot += self.small_blind_value
        self.players[self.big_blind_player].bank_account.call(self.big_blind_value)
        self.pot += self.big_blind_value

    # TODO FINISHED
    def update_players_bank_after_mini_game(self, names):  # TODO name will be array of the winners and amount
        for key in self.players.keys():
            self.players[key].bank_account.fold()


    def winner(self):
        winners = []
        text = ""
        players_to_choose_from = []
        for key in self.players.keys():
            if self.players[key].status != Status.FOLDED.value:
                players_to_choose_from.append(key)

        group_by_invest = {}
        if len(players_to_choose_from) != 1:
            for name in players_to_choose_from:  # set the dict with key of iveste and empy array
                group_by_invest[self.players[name].bank_account.mini_game_invested] = []
            for name in players_to_choose_from:  # insert values to the array
                group_by_invest[self.players[name].bank_account.mini_game_invested].append(
                    {'name': name, 'hand_rank': self.players[name].hand.calculate_strength(self.cards_on_the_table),
                     'money_invest': self.players[name].bank_account.mini_game_invested})
            # TODO will need to add the case if there are two peple with same hand power with the same invest
            for key in group_by_invest.keys():
                max_rank = 0
                for player in group_by_invest[key]:
                    if max_rank < player['hand_rank']:
                        max_rank = player['hand_rank']
                i = len(group_by_invest[key]) - 1
                while i >= 0:
                    if group_by_invest[key][i]['hand_rank'] != max_rank:
                        group_by_invest[key].remove(group_by_invest[key][i])
                    i -= 1
            players_to_choose_from = []
            for key in group_by_invest.keys():
                players_to_choose_from = np.concatenate((players_to_choose_from, group_by_invest[key]))
            player_ordered_by_rank = sorted(players_to_choose_from, key=sort_rank_array, reverse=True)
            player_ordered_by_invest = sorted(players_to_choose_from, key=sort_invest_array, reverse=True)
            invest_counts = defaultdict(lambda: 0)
            for p in players_to_choose_from:
                invest_counts[p['money_invest']] += 1
            hand_rank_counts = defaultdict(lambda: 0)
            for p in players_to_choose_from:
                hand_rank_counts[p['hand_rank']] += 1
            while len(player_ordered_by_rank) != 0:
                player_to_check = player_ordered_by_rank[0]
                pot_for_the_winner = 0
                if hand_rank_counts[player_to_check['hand_rank']] == 1:
                    for key in self.players.keys():
                        if self.players[key].bank_account.mini_game_invested <= player_to_check['money_invest']:
                            pot_for_the_winner += self.players[key].bank_account.mini_game_invested
                            if contained(key, player_ordered_by_rank):
                                player_ordered_by_invest = filter_array(player_ordered_by_invest, key)
                                player_ordered_by_rank = filter_array(player_ordered_by_rank, key)
                            self.players[key].bank_account.fold()
                    self.players[player_to_check['name']].bank_account.won_mini_game_update(pot_for_the_winner)
                    text += "the name of the player , hand rank and pot"
                else:
                    None  # TODO more then one person with same rank
            return players_to_choose_from

    # TODO FINISHED
    def switch_to_next_player(self):

        while True:
            if self.is_last_player_folded:
                if self.folded_player_index <= len(self.players_remaining) - 1:
                    self.current_player = self.players_remaining[self.folded_player_index]
                else:
                    self.current_player = self.players_remaining[0]
                if self.players[self.current_player].status != Status.ALL_IN.value:
                    return
            else:
                self.current_player = self.players_remaining[
                    (self.players_remaining.index(self.current_player) + 1) % len(self.players_remaining)]
                if self.players[self.current_player].status != Status.ALL_IN.value:
                    return

    ############# ROUND METHODS ###################
    # TODO FINISHED
    def new_round(self):
        self.open_new_card()
        for key in self.players.keys():
            if self.players[key].status != Status.FOLDED.value and self.players[key].status != Status.ALL_IN.value:
                self.players[key].status = Status.WAIT_FOR_TURN.value

    # the idea check if every one in the table is check or everyone is check and the next player is rasied
    # TODO FINISHED
    def is_round_over(self):
        if self.is_last_player_folded:
            if self.folded_player_index <= len(self.players_remaining) - 1:
                next_player_name = self.players_remaining[self.folded_player_index]
            else:
                next_player_name = self.players_remaining[0]
        else:
            next_player_name = self.players_remaining[
                (self.players_remaining.index(self.current_player) + 1) % len(self.players_remaining)]
        if self.players[next_player_name].status == Status.RAISED.value:
            for n in self.players_remaining:
                if self.players[n].status != Status.CALLED.value and n != next_player_name:
                    return False
        else:
            for n in self.players_remaining:
                if self.players[n].status != Status.CHECKED.value:
                    return False
        return True

    # TODO FINISHED
    ########### MINI GAME METHODS ###############
    def new_mini_game(self):
        for key in self.players.keys():
            if self.players[key].bank_account.total_cash > 0:
                self.players_remaining.append(self.players[key].name)
                self.players[key].status = Status.WAIT_FOR_TURN.value
        self.deck = Deck()
        self.pot = 0
        if self.small_blind_player == "":
            self.init_buttons()
        else:
            self.update_buttons()
        self.deck.deal_cards(self.players)
        self.collect_blinds()
        self.run_game()

    # TODO FINISHED
    def end_mini_game(self):
        self.winner()
        self.players_remaining = []
        self.cards_on_the_table = []
        self.new_mini_game()

    # TODO FINISHED
    def is_mini_game_over(self):
        if (len(self.cards_on_the_table) == 5 and self.is_round_over()) or len(
                self.players_remaining) == 1:  # TODO try en(self.cards_on_the_table) == 6
            return True
        else:
            return False

    ############# PRINT METHODS #################
    # TODO FINISHED
    def table_status(self):
        text = ''
        players_cash = ""
        table_cards = "Card On The Table: "
        text += f'Pot: {self.pot}\n'
        text += f'Dealer Button: {self.dealer_button_player}\n'
        text += f'Small Blind: {self.small_blind_player}\n'
        text += f'Big Blind: {self.big_blind_player}\n'
        for i in range(0, len(self.cards_on_the_table)):
            table_cards += f'{self.cards_on_the_table[i].print_card()} ,'
        text += f'{table_cards}\n'
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
                (self.players_remaining.index(self.dealer_button_player) + 1) % len(self.players_remaining)]
            self.small_blind_player = self.players_remaining[
                (self.players_remaining.index(self.small_blind_player) + 1) % len(self.players_remaining)]
            self.big_blind_player = self.players_remaining[
                (self.players_remaining.index(self.big_blind_player) + 1) % len(self.players_remaining)]
            self.current_player = self.players_remaining[
                (self.players_remaining.index(self.dealer_button_player) + 1) % len(self.players)]
            self.player_who_started_the_round = self.players_remaining[
                (self.players_remaining.index(self.dealer_button_player) + 1) % len(self.players)]


def sort_rank_array(val):
    return val['hand_rank']


def sort_invest_array(val):
    return val['money_invest']


def contained(val, array):
    for player in array:
        if player['name'] == val:
            return True
    return False


def filter_array(players, name):
    i = len(players) - 1
    while i >= 0:
        if players[i]["name"] == name:
            players.remove(players[i])
        i = i - 1
    return players
