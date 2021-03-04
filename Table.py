from Deck import Deck
from Enums import Status
import threading
from Player import Player
import numpy as np

lock = threading.Lock()


class Table:
    def __init__(self, small_blind_value, big_blind_value, starting_cash):
        self.did_all_in_in_this_round = []
        self.mini_game_pots = {}
        self.players = {}
        self.players_remaining = []
        self.small_blind_player = ""
        self.big_blind_player = ""
        self.dealer_button_player = ""
        self.small_blind_value = small_blind_value
        self.big_blind_value = big_blind_value
        self.deck = Deck()
        self.cards_on_the_table = []
        self.current_player = ""
        self.starting_cash = starting_cash
        self.is_last_player_folded = False
        self.folded_player_index = None

    def player_action(self, action):
        actions_parts = action.split()
        if actions_parts[0].lower() == "check":
            self.is_last_player_folded = False
            self.folded_player_index = 0
            self.players[self.current_player].status = Status.CHECKED.value
            self.complete_player_turn_and_switch_player()
            return True
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
            if self.players[self.current_player].bank_account.need_all_in(max_raise_yet):
                self.players[self.current_player].status = Status.ALL_IN.value
                self.did_all_in_in_this_round.append(self.current_player)
            self.players[self.current_player].bank_account.call(
                max_raise_yet - self.players[self.current_player].bank_account.round_invested)
            self.is_last_player_folded = False
            self.folded_player_index = 0
            self.complete_player_turn_and_switch_player()
            return True
        elif actions_parts[0].lower() == "raise" and len(actions_parts) == 2 and actions_parts[1].isnumeric():
            self.players[self.current_player].status = Status.RAISED.value  # TODO "FOLD" LOOKS LIKE ITS FINISHED
            self.players[self.current_player].bank_account.raise_bet(actions_parts[1])
            self.is_last_player_folded = False
            self.folded_player_index = 0
            self.complete_player_turn_and_switch_player()
            return True
        return False

    def complete_player_turn_and_switch_player(self):
        all_players_all_in_or_fold = True
        for key in self.players.keys():
            if self.players[key].status != Status.ALL_IN.value and self.players[key].status != Status.FOLDED.value:
                all_players_all_in_or_fold = False
        if self.is_mini_game_over():
            self.end_mini_game()
        elif self.is_round_over() and all_players_all_in_or_fold:
            self.open_rest_of_cards()
            self.end_mini_game()
        elif self.is_round_over() and len(self.did_all_in_in_this_round) > 0:
            self.update_pot()
            print(self.mini_game_pots)
            self.new_round()
        elif self.is_round_over():
            self.new_round()

        self.switch_to_next_player()
        return

    ############## TABLE METHODS #################
    def register_player(self, name):
        lock.acquire()
        if name == "Omri":
            player = Player(name, 3000)
        if name == "Bar":
            player = Player(name, 2000)
        if name == "Ido":
            player = Player(name, 1000)
        # player = Player(name, self.starting_cash)
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
                f'{self.current_player} turn:\nHand:{self.players[self.current_player].hand.print_hand()}\n\nEnter your action:\nActions:\n{check_option if not someone_raised else ""}FOLD: fold\nCALL: call\nRAISE: raise 100\n')
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
        self.players[self.big_blind_player].bank_account.call(self.big_blind_value)

    def winner(self):
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
            player_ordered_by_invest = sorted(players_to_choose_from, key=sort_invest_array, reverse=True)
            counter = len(player_ordered_by_invest) - 1
            i = len(player_ordered_by_invest) - 1
            while counter >= 0:
                while i >= 1:
                    if player_ordered_by_invest[i]['hand_rank'] < player_ordered_by_invest[i - 1]['hand_rank']:
                        player_ordered_by_invest.remove(player_ordered_by_invest[i])
                    i -= 1
                counter -= 1
            player_ordered_by_invest = sorted(player_ordered_by_invest, key=sort_invest_array)
            last_value = 0  # to same last key value
            for key in self.mini_game_pots.keys():
                had_player_with_this_invest = False
                for player in player_ordered_by_invest:
                    if player['money_invest'] == key:
                        had_player_with_this_invest = True
                        break
                if had_player_with_this_invest:
                    self.mini_game_pots[key] += last_value
                    last_value = 0
                else:
                    last_value = self.mini_game_pots[key]
                    self.mini_game_pots[key] = 0
            self.mini_game_pots = {x: y for x, y in self.mini_game_pots.items() if y != 0}
            while len(player_ordered_by_invest) != 0:
                player_to_check = player_ordered_by_invest[0]
                players_names_to_split_with = []
                for player in player_ordered_by_invest:
                    if player['hand_rank'] >= player_to_check['hand_rank']:
                        players_names_to_split_with.append(player['name'])

                for player in players_names_to_split_with:
                    self.players[player].bank_account.won_game_update(
                        self.mini_game_pots[player_to_check['money_invest']] / len(players_names_to_split_with))
                player_ordered_by_invest = remove_all_players_with_same_investment(player_ordered_by_invest,
                                                                                   player_to_check['money_invest'])

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
            while self.players[next_player_name].status == Status.ALL_IN.value:  # pass the all in players
                next_player_name = self.players_remaining[
                    (self.players_remaining.index(next_player_name) + 1) % len(self.players_remaining)]
        if self.players[next_player_name].status == Status.RAISED.value:
            for n in self.players_remaining:
                if (self.players[n].status != Status.CALLED.value and self.players[
                    n].status != Status.ALL_IN.value) and n != next_player_name:
                    return False
        else:
            for n in self.players_remaining:
                if self.players[n].status != Status.CHECKED.value and self.players[n].status != Status.ALL_IN.value:
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
        if self.small_blind_player == "":
            self.init_buttons()
        else:
            self.update_buttons()
        self.deck.deal_cards(self.players)
        self.collect_blinds()
        self.run_game()

    # TODO FINISHED
    def end_mini_game(self):
        if len(self.mini_game_pots) == 0:
            self.create_one_pot_for_all()
        else:
            self.create_left_over_pot()
        self.winner()
        self.winner_status()
        self.update_losers()
        self.mini_game_pots = {}
        self.players_remaining = []
        self.cards_on_the_table = []
        self.new_mini_game()

    # TODO FINISHED
    def is_mini_game_over(self):
        if (len(self.cards_on_the_table) == 5 and self.is_round_over()) or len(
                self.players_remaining) == 1:
            return True
        else:
            return False

    ############# PRINT METHODS #################
    # TODO FINISHED
    def table_status(self):
        text = ''
        players_cash = ""
        table_cards = "Card On The Table: "
        text += f'Pot: {self.pot_calc()}\n'
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
            self.current_player = self.players_remaining[0]

        else:
            self.dealer_button_player = self.players_remaining[0]
            self.small_blind_player = self.players_remaining[1]
            self.big_blind_player = self.players_remaining[2]
            self.current_player = self.players_remaining[0]

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
                (self.players_remaining.index(self.dealer_button_player) + 1) % len(self.players_remaining)]
            self.small_blind_player = self.players_remaining[
                (self.players_remaining.index(self.small_blind_player) + 1) % len(self.players_remaining)]
            self.big_blind_player = self.players_remaining[
                (self.players_remaining.index(self.big_blind_player) + 1) % len(self.players_remaining)]
            self.current_player = self.players_remaining[
                (self.players_remaining.index(self.dealer_button_player) + 1) % len(self.players)]

    def open_rest_of_cards(self):
        if len(self.cards_on_the_table) == 0:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_flop()))
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_turn()))
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))
        elif len(self.cards_on_the_table) == 3:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_turn()))
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))
        elif len(self.cards_on_the_table) == 5:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))

    def update_pot(self):
        players_all_in = {}
        for name in self.did_all_in_in_this_round:
            players_all_in[self.players[name].bank_account.mini_game_invested] = []
        for name in self.did_all_in_in_this_round:
            players_all_in[self.players[name].bank_account.mini_game_invested].append(name)
        for invest in sorted(players_all_in.keys()):
            pot = 0
            for key in self.players.keys():
                if self.players[key].bank_account.mini_game_invested >= invest:
                    pot += invest
                else:
                    pot += self.players[key].bank_account.mini_game_invested
            for key in self.mini_game_pots.keys():
                pot -= self.mini_game_pots[key]
            self.mini_game_pots[invest] = pot
        self.did_all_in_in_this_round = []

    def update_losers(self):
        for key in self.players.keys():
            self.players[key].bank_account.lost_game_update()
        self.players = self.remove_all_players_with_zero_cash()

    def winner_status(self):
        text = "WINNERS:\n"
        for key in self.players.keys():
            if self.players[key].bank_account.mini_game_eared > 0:
                text += f'{key}: won {self.players[key].bank_account.mini_game_eared} with hank rank of:{self.players[key].hand.calculate_strength(self.cards_on_the_table)}\n'

        print(text)

    def create_one_pot_for_all(self):
        pot = 0
        for key in self.players.keys():
            pot += self.players[key].bank_account.mini_game_invested
        self.mini_game_pots[self.players[self.players_remaining[0]].bank_account.mini_game_invested] = pot

    def pot_calc(self):
        pot = 0
        for key in self.players.keys():
            pot += self.players[key].bank_account.mini_game_invested
        return pot

    def create_left_over_pot(self):
        max_invest = 0
        pot = 0

        for name in self.players_remaining:
            if self.players[name].bank_account.mini_game_invested > max_invest:
                max_invest = self.players[name].bank_account.mini_game_invested
        for key in self.players.keys():
            if self.players[key].bank_account.mini_game_invested >= max_invest:
                pot += max_invest
            else:
                pot += self.players[key].bank_account.mini_game_invested
        for key in self.mini_game_pots.keys():
            pot -= self.mini_game_pots[key]
        self.mini_game_pots[max_invest] = pot
        self.did_all_in_in_this_round = []

    def remove_all_players_with_zero_cash(self):
        new_array = {}
        for key in self.players:
            if self.players[key].bank_account.total_cash != 0:
                new_array[key] = self.players[key]
        return new_array


def sort_rank_array(val):
    return val['hand_rank']


def sort_invest_array(val):
    return val['money_invest']


def contained(val, array):
    for player in array:
        if player['name'] == val:
            return True
    return False


def remove_all_players_with_same_investment(players_ordered_by_invest, value):
    new_array = []
    for player in players_ordered_by_invest:
        if player['money_invest'] != value:
            new_array.append(player)

    return new_array


def filter_array(players, name):
    i = len(players) - 1
    while i >= 0:
        if players[i]["name"] == name:
            players.remove(players[i])
        i = i - 1
    return players
