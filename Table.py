from random import randrange

from Deck import Deck
from Enums import Status, TableStatus, TestMode
import threading
from Player import Player
import numpy as np

lock = threading.Lock()


class Table:
    def __init__(self, small_blind_value, big_blind_value, starting_cash, test_mode, index_file):
        # for auto testing
        self.test_mode = test_mode
        if test_mode == TestMode.AUTOMATICALLY.value:
            self.simulation = open(f'testing/scenes/simulation{index_file}.txt', "r")
        # table info
        self.table_status = TableStatus.WAIT_FOR_PLAYERS.value
        self.names_of_players_who_all_in_this_round = []
        self.game_pots = []
        self.players = {}  # {{key:name1 ,value:Player()},{key:name2 ,value:Player()}}
        self.names_of_players_remaining = []
        self.small_blind_player_name = ""
        self.big_blind_player_name = ""
        self.dealer_button_player_name = ""
        self.small_blind_value = small_blind_value
        self.big_blind_value = big_blind_value
        self.deck = Deck()
        self.cards_on_the_table = []
        self.current_player_name = ""
        self.starting_cash = starting_cash
        self.is_last_player_folded = False
        self.folded_player_index = None
        self.current_index = None

    def player_action(self, command_parts):
        print(f'{self.current_player_name} is {command_parts["action"]}')
        if command_parts['action'] == "check":
            self.is_last_player_folded = False
            self.folded_player_index = 0
            self.players[self.current_player_name].status = Status.CHECKED.value


        elif command_parts['action'] == "fold":
            self.is_last_player_folded = True
            self.folded_player_index = self.names_of_players_remaining.index(self.current_player_name)
            self.players[self.current_player_name].status = Status.FOLDED.value  # TODO "FOLD" LOOKS LIKE ITS FINISHED
            self.names_of_players_remaining.remove(self.current_player_name)



        elif command_parts['action'] == "call":  # TODO "CALL" LOOKS LIKE ITS FINISHED
            player_name_with_max_raise = max(self.names_of_players_remaining,
                                             key=lambda k: self.players[k].bank_account.round_investment)
            max_raise_yet = self.players[player_name_with_max_raise].bank_account.round_investment
            self.players[self.current_player_name].status = Status.CALLED.value
            if self.players[self.current_player_name].bank_account.need_all_in(max_raise_yet):
                self.players[self.current_player_name].status = Status.CALL_ALL_IN.value
                self.names_of_players_who_all_in_this_round.append(self.current_player_name)
            self.players[self.current_player_name].bank_account.call(
                max_raise_yet - self.players[self.current_player_name].bank_account.round_investment)
            self.is_last_player_folded = False
            self.folded_player_index = 0

        elif command_parts['action'].lower() == "raise":
            player_name_with_max_raise = max(self.names_of_players_remaining,
                                             key=lambda k: self.players[k].bank_account.round_investment)
            max_invest_available_from_other_player = 0
            for key in self.players:
                if key != self.current_player_name:
                    if self.players[key].bank_account.round_investment + self.players[
                        key].bank_account.max_bet_allowed > max_invest_available_from_other_player:
                        max_invest_available_from_other_player = self.players[key].bank_account.round_investment + \
                                                                 self.players[key].bank_account.max_bet_allowed

            max_raise = self.players[player_name_with_max_raise].bank_account.round_investment
            if self.players[self.current_player_name].bank_account.max_bet_allowed + self.players[
                self.current_player_name].bank_account.round_investment == max_raise + int(command_parts['invest']):
                self.players[
                    self.current_player_name].status = Status.RAISE_ALL_IN.value  # TODO "FOLD" LOOKS LIKE ITS FINISHED
                self.players[self.current_player_name].bank_account.raise_bet(
                    max_raise + int(command_parts['invest']) - self.players[
                        self.current_player_name].bank_account.round_investment)
            elif max_raise + int(command_parts['invest']) > max_invest_available_from_other_player:
                self.players[self.current_player_name].status = Status.RAISED.value
                self.players[self.current_player_name].bank_account.raise_bet(
                    max_invest_available_from_other_player - self.players[
                        self.current_player_name].bank_account.round_investment)
            else:
                self.players[self.current_player_name].status = Status.RAISED.value
                self.players[self.current_player_name].bank_account.raise_bet(
                    max_raise + int(command_parts['invest']) - self.players[
                        self.current_player_name].bank_account.round_investment)
            self.is_last_player_folded = False
            self.folded_player_index = 0

    def complete_player_turn(self):
        all_players_all_in_or_fold = True
        raise_counter = 0
        for key in self.players.keys():
            if self.players[key].status == Status.RAISED.value:
                raise_counter += 1
            elif self.players[key].status != Status.ALL_IN.value and \
                    self.players[key].status != Status.CALL_ALL_IN.value and \
                    self.players[key].status != Status.RAISE_ALL_IN.value and \
                    self.players[key].status != Status.FOLDED.value:
                all_players_all_in_or_fold = False

        if self.is_mini_game_over():
            self.table_status = TableStatus.GAME_FINISHED.value
        elif self.is_round_over() and all_players_all_in_or_fold and raise_counter <= 1:
            self.open_rest_of_cards()
            self.table_status = TableStatus.GAME_FINISHED.value
        elif self.is_round_over() and len(self.names_of_players_who_all_in_this_round) > 0:
            self.table_status = TableStatus.STARTING_NEW_ROUND.value
            self.all_in_split_pot()
            self.end_round()
        elif self.is_round_over():
            self.end_round()
            self.table_status = TableStatus.STARTING_NEW_ROUND.value
        if len(self.players) == 1:
            self.table_status = TableStatus.TABLE_FINISHED.value

    ############## TABLE METHODS #################
    def register_player(self, name):
        lock.acquire()
        # if name == "Omri":
        #     player = Player(name, 3000)
        # if name == "Bar":
        #     player = Player(name, 2000)
        # if name == "Ido":
        #     player = Player(name, 1000)
        player = Player(name, self.starting_cash)
        self.players[name] = player
        lock.release()

    def init_table(self):
        while self.table_status != TableStatus.TABLE_FINISHED.value:
            self.set_table_for_new_game()
            self.table_status = TableStatus.RUNNING.value
            self.run_game()
            self.end_game()
        return

    def player_input(self):
        someone_raised = False
        for key in self.players.keys():
            if self.players[key].status == Status.RAISED.value or \
                    self.players[key].status == Status.RAISE_ALL_IN.value or \
                    self.players[key].status == Status.SMALL_BLIND.value or \
                    self.players[key].status == Status.BIG_BLIND.value:
                someone_raised = True
        check_option = "CHECK: check\n"
        call_option = "CALL: call\n"
        player_name_with_max_raise = max(self.names_of_players_remaining,
                                         key=lambda k: self.players[k].bank_account.round_investment)
        max_raise = self.players[player_name_with_max_raise].bank_account.round_investment
        if self.test_mode == TestMode.AUTOMATICALLY.value:
            command = self.simulation.readline()[:-1]
        else:
            command = input(
                f'{self.current_player_name} turn:\nHand:{self.players[self.current_player_name].hand.print_hand()}\n\nEnter your action:\nActions:\n{check_option if not someone_raised else ""}{call_option if someone_raised else ""}FOLD: fold\nRAISE: raise 100\n')
        command_parts = command.split()
        if len(command_parts) == 1:
            command_parts = {'action': command_parts[0].lower()}
        if len(command_parts) == 2:
            command_parts = {'action': command_parts[0].lower(), 'invest': command_parts[1]}
        if len(command_parts) >= 3:
            print(f'Error:too long input')
        elif command_parts['action'] == "raise" and len(command_parts) == 2 and command_parts[
            'invest'].isnumeric() and \
                self.players[self.current_player_name].bank_account.max_bet_allowed < max_raise + int(
            command_parts['invest']):
            print(f'Error:try raise over max bet available')
            return "error"
        elif command_parts['action'] == "call" and not someone_raised:
            print(f'Error:cant call when no one raised')
            return "error"

        elif command_parts['action'] == "check" and someone_raised:
            print(f'Error:cant check when someone raised')
            return "error"

        elif command_parts['action'] != "check" and command_parts['action'] != "raise" and command_parts[
            'action'] != "call":
            print(f'Error: not illegal command')
            return "error"
        else:
            return command_parts

    def run_game(self):
        print_state_table = True
        while self.table_status != TableStatus.GAME_FINISHED.value:
            if print_state_table:
                self.print_table_status()
            print_state_table = True
            command_parts = self.player_input()
            if command_parts == "error":
                print_state_table = False
            else:
                self.player_action(command_parts)
                self.complete_player_turn()
                if self.table_status == TableStatus.STARTING_NEW_ROUND.value:
                    self.new_round()
                    self.table_status = TableStatus.RUNNING.value
                if self.table_status != TableStatus.GAME_FINISHED.value:
                    self.switch_to_next_player()

    def open_new_card(self):
        if len(self.cards_on_the_table) == 0:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_flop()))
        elif len(self.cards_on_the_table) == 3:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_turn()))
        elif len(self.cards_on_the_table) == 4:
            self.cards_on_the_table = np.concatenate((self.cards_on_the_table, self.deck.the_river()))

    # TODO FINISHED
    def collect_blinds(self):
        self.players[self.small_blind_player_name].bank_account.call(self.small_blind_value)

        self.players[self.big_blind_player_name].bank_account.call(self.big_blind_value)

    def winner(self):
        players_to_choose_from = [key for key in self.players.keys() if self.players[key].status != Status.FOLDED.value]
        group_by_invest = {}
        if len(players_to_choose_from) != 1:
            for name in players_to_choose_from:  # set the dict with key of invested and empty array
                group_by_invest[self.players[name].bank_account.mini_game_investment] = []
            for name in players_to_choose_from:  # insert values to the array
                group_by_invest[self.players[name].bank_account.mini_game_investment].append(
                    {'name': name, 'hand_rank': self.players[name].hand.rank_score(self.cards_on_the_table)['rank_score'],
                     'money_invest': self.players[name].bank_account.mini_game_investment})
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
            for pot in self.game_pots:
                had_player_with_this_invest = False
                for player in player_ordered_by_invest:
                    if player['money_invest'] == pot['invest']:
                        had_player_with_this_invest = True
                        break
                if had_player_with_this_invest:
                    pot['reward'] += last_value
                    last_value = 0
                else:
                    last_value = pot['reward']
                    pot['reward'] = 0
            if len(self.game_pots) > 0:
                self.game_pots = [pot for pot in self.game_pots if pot['reward'] != 0]

            while len(player_ordered_by_invest) != 0:
                player_to_check = player_ordered_by_invest[0]
                pot_to_split = [pot['reward'] for pot in self.game_pots if
                                pot['invest'] == player_to_check['money_invest']][0]
                players_names_to_split_with = [player for player in player_ordered_by_invest if
                                               player['hand_rank'] >= player_to_check['hand_rank']]
                for player in players_names_to_split_with:
                    self.players[player['name']].bank_account.won_game_update(int(
                        pot_to_split / len(players_names_to_split_with)))
                player_ordered_by_invest = remove_all_players_with_same_investment(player_ordered_by_invest,
                                                                                   player_to_check['money_invest'])
                for pot in self.game_pots:
                    if pot['invest'] == player_to_check['money_invest']:
                        self.game_pots.remove(pot)

    # TODO FINISHED
    def switch_to_next_player(self):

        while True:
            if self.is_last_player_folded:
                if self.folded_player_index <= len(self.names_of_players_remaining) - 1:
                    self.current_player_name = self.names_of_players_remaining[self.folded_player_index]
                else:
                    self.current_player_name = self.names_of_players_remaining[0]
            else:
                self.current_player_name = self.names_of_players_remaining[
                    (self.names_of_players_remaining.index(self.current_player_name) + 1) % len(
                        self.names_of_players_remaining)]
            if self.players[self.current_player_name].status != Status.ALL_IN.value and self.players[
                self.current_player_name].status != Status.RAISE_ALL_IN.value and self.players[
                self.current_player_name].status != Status.CALL_ALL_IN.value:
                return

    ############# ROUND METHODS ###################
    # TODO FINISHED
    def new_round(self):
        for name in self.names_of_players_remaining:
            self.players[name].bank_account.new_round()
        self.open_new_card()
        for key in self.players.keys():
            if self.players[key].status == Status.RAISE_ALL_IN.value or self.players[
                key].status == Status.CALL_ALL_IN.value:
                self.players[key].status = Status.ALL_IN.value
            if self.players[key].status != Status.FOLDED.value and self.players[key].status != Status.ALL_IN.value:
                self.players[key].status = Status.WAIT_FOR_TURN.value

    # the idea check if every one in the table is check or everyone is check and the next player is raised
    # TODO FINISHED
    def is_round_over(self):
        if self.is_last_player_folded:
            if self.folded_player_index <= len(self.names_of_players_remaining) - 1:
                next_player_name = self.names_of_players_remaining[self.folded_player_index]
            else:
                next_player_name = self.names_of_players_remaining[0]
        else:
            next_player_name = self.names_of_players_remaining[
                (self.names_of_players_remaining.index(self.current_player_name) + 1) % len(
                    self.names_of_players_remaining)]
            while self.players[next_player_name].status == Status.ALL_IN.value or self.players[
                next_player_name].status == Status.CALL_ALL_IN.value:  # pass the all in players
                next_player_name = self.names_of_players_remaining[
                    (self.names_of_players_remaining.index(next_player_name) + 1) % len(
                        self.names_of_players_remaining)]
        if self.players[next_player_name].status == Status.RAISED.value or self.players[
            next_player_name].status == Status.RAISE_ALL_IN.value:  # if there are more then 2 raise
            for n in self.names_of_players_remaining:
                if self.players[n].status != Status.CALL_ALL_IN.value and self.players[
                    n].status != Status.CALLED.value and self.players[
                    n].status != Status.ALL_IN.value and n != next_player_name:
                    return False
        else:
            for n in self.names_of_players_remaining:  # in not
                if self.players[n].status != Status.CHECKED.value and self.players[n].status != Status.ALL_IN.value:
                    return False
        return True

    # TODO FINISHED
    ########### MINI GAME METHODS ###############
    def set_table_for_new_game(self):
        for key in self.players.keys():
            self.names_of_players_remaining.append(self.players[key].name)
        if self.small_blind_player_name == "":
            self.init_buttons()
        else:
            self.update_buttons()
        for key in self.players.keys():
            if self.small_blind_player_name == key:
                self.players[key].status = Status.SMALL_BLIND.value
            elif self.big_blind_player_name == key:
                self.players[key].status = Status.BIG_BLIND.value
            elif self.dealer_button_player_name == key:
                self.players[key].status = Status.DEALER.value
            else:
                self.players[key].status = Status.WAIT_FOR_TURN.value

        self.deck = Deck()

        self.deck.deal_cards(self.players)
        self.collect_blinds()

        # TODO FINISHED

    def end_round(self):
        self.names_of_players_who_all_in_this_round = []

    def end_game(self):
        if len(self.game_pots) == 0 and len(self.names_of_players_who_all_in_this_round) == 0:
            self.create_single_pot_for_all_players()
        elif len(self.game_pots) == 0 and len(self.names_of_players_who_all_in_this_round) != 0:
            self.all_in_split_pot()
            self.create_left_over_pot()
        else:
            self.create_left_over_pot()
        self.names_of_players_who_all_in_this_round = []
        self.winner()
        self.winner_status()
        self.update_losers()
        self.game_pots = []
        self.names_of_players_remaining = []
        self.cards_on_the_table = []
        self.table_status = TableStatus.STARTING_NEW_GAME.value
        if len(self.players) == 1:
            self.table_status = TableStatus.TABLE_FINISHED.value

    # TODO FINISHED
    def is_mini_game_over(self):
        if (len(self.cards_on_the_table) == 5 and self.is_round_over()) or len(
                self.names_of_players_remaining) == 1:
            return True
        else:
            return False

    ############# PRINT METHODS #################
    # TODO FINISHED
    def print_table_status(self):
        text = ''
        players_cash = ""
        table_cards = "Card On The Table: "
        text += f'Pot: {self.pot_calc()}\n'
        text += f'Dealer Button: {self.dealer_button_player_name if len(self.names_of_players_remaining) > 2 else "NOT IN USE"}\n'
        text += f'Small Blind: {self.small_blind_player_name}\n'
        text += f'Big Blind: {self.big_blind_player_name}\n'
        for i in range(0, len(self.cards_on_the_table)):
            table_cards += f'{self.cards_on_the_table[i].print_card()} ,'
        text += f'{table_cards}\n'
        for key in self.players.keys():
            players_cash += f'{self.players[key].name}:\tCash In hand:{self.players[key].bank_account.max_bet_allowed},\tCash In in Pot:{self.players[key].bank_account.mini_game_investment},\tCash Invest In Round:{self.players[key].bank_account.round_investment},\tStatus:{self.players[key].status}\n'
        text += players_cash
        print(text)

    ################ GETTERS ###################
    # TODO FINISHED
    def get_player_hand(self, name):
        return self.players[name].hand

    ############## BUTTON METHODS ##############
    # TODO FINISHED
    def init_buttons(self):
        random_play_index = randrange(len(self.names_of_players_remaining))
        if len(self.names_of_players_remaining) == 2:
            self.small_blind_player_name = self.names_of_players_remaining[
                random_play_index % len(self.names_of_players_remaining)]
            self.big_blind_player_name = self.names_of_players_remaining[
                (random_play_index + 1) % len(self.names_of_players_remaining)]
            self.current_player_name = self.small_blind_player_name
            self.dealer_button_player_name = "NO NEED"
        else:
            self.dealer_button_player_name = self.names_of_players_remaining[
                random_play_index % len(self.names_of_players_remaining)]
            self.small_blind_player_name = self.names_of_players_remaining[
                (random_play_index + 1) % len(self.names_of_players_remaining)]
            self.big_blind_player_name = self.names_of_players_remaining[
                (random_play_index + 2) % len(self.names_of_players_remaining)]
            self.current_player_name = self.dealer_button_player_name

    # TODO FINISHED
    def update_buttons(self):
        if len(self.names_of_players_remaining) == 2:
            if self.small_blind_player_name != self.names_of_players_remaining[0]:
                self.small_blind_player_name = self.names_of_players_remaining[0]
                self.big_blind_player_name = self.names_of_players_remaining[1]
                self.current_player_name = self.names_of_players_remaining[0]
                self.dealer_button_player_name = "NO NEED"
            else:
                self.small_blind_player_name = self.names_of_players_remaining[1]
                self.big_blind_player_name = self.names_of_players_remaining[0]
                self.current_player_name = self.names_of_players_remaining[1]
                self.dealer_button_player_name = "NO NEED"
        elif len(self.names_of_players_remaining) > 2:
            self.dealer_button_player_name = self.names_of_players_remaining[
                (self.names_of_players_remaining.index(self.dealer_button_player_name) + 1) % len(
                    self.names_of_players_remaining)]
            self.small_blind_player_name = self.names_of_players_remaining[
                (self.names_of_players_remaining.index(self.small_blind_player_name) + 1) % len(
                    self.names_of_players_remaining)]
            self.big_blind_player_name = self.names_of_players_remaining[
                (self.names_of_players_remaining.index(self.big_blind_player_name) + 1) % len(
                    self.names_of_players_remaining)]
            self.current_player_name = self.names_of_players_remaining[
                (self.names_of_players_remaining.index(self.dealer_button_player_name)) % len(self.players)]

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
        table_cards = "Card On The Table: "
        for i in range(0, len(self.cards_on_the_table)):
            table_cards += f'{self.cards_on_the_table[i].print_card()} ,'

    def all_in_split_pot(self):
        players_all_in = {}
        for name in self.names_of_players_who_all_in_this_round:
            players_all_in[self.players[name].bank_account.mini_game_investment] = []
        for name in self.names_of_players_who_all_in_this_round:
            players_all_in[self.players[name].bank_account.mini_game_investment].append(name)
        for invest in sorted(players_all_in.keys()):
            reward = 0
            for key in self.players.keys():
                if self.players[key].bank_account.mini_game_investment >= invest:
                    reward += invest
                else:
                    reward += self.players[key].bank_account.mini_game_investment
            for pot in self.game_pots:

                reward -= pot['reward']
            self.game_pots.append({'invest': invest, 'reward': reward})

    def update_losers(self):
        for key in self.players.keys():
            self.players[key].bank_account.after_game_update()
        self.players = self.remove_all_players_with_zero_cash()

    def winner_status(self):
        text = "WINNERS:\n"
        for key in self.players.keys():

            if self.players[key].bank_account.mini_game_eared > 0:
                text += f'{key} won {self.players[key].bank_account.mini_game_eared} cash with {self.players[key].hand.rank_score(self.cards_on_the_table)["rank_name"]}\n'

        print(text)
        players_hands = "All Players hands:\n"
        for key in self.players.keys():
            player_hand = "("
            for card in self.players[key].hand.rank_score(self.cards_on_the_table)['hand']:
                player_hand += f'{card.print_card()}'
            player_hand += f')'
            players_hands += f'{key} Hand:{player_hand}\n'
        print(players_hands)

    def create_single_pot_for_all_players(self):
        print(f'game pots before update in "single pot for all" {self.game_pots}')

        pot = 0
        for key in self.players.keys():
            pot += self.players[key].bank_account.mini_game_investment
        self.game_pots.append(
            {"invest": self.players[self.names_of_players_remaining[0]].bank_account.mini_game_investment,
             'reward': pot})
        print(f'game pots after update in "single pot for all" {self.game_pots}')

    def pot_calc(self):
        pot = 0
        for key in self.players.keys():
            pot += self.players[key].bank_account.mini_game_investment
        return pot

    def create_left_over_pot(self):

        pot = 0
        max_invest_name = max(self.names_of_players_remaining,
                              key=lambda k: self.players[k].bank_account.mini_game_investment)
        max_invest = self.players[max_invest_name].bank_account.mini_game_investment
        for key in self.players.keys():
            pot += self.players[key].bank_account.mini_game_investment
        for p in self.game_pots:
            pot -= p['reward']
        self.game_pots.append({'invest': max_invest, 'reward': pot})

    def remove_all_players_with_zero_cash(self):
        new_array = {}
        for key in self.players:
            if self.players[key].bank_account.total_cash != 0:
                new_array[key] = self.players[key]
            if self.players[key].bank_account.total_cash == 0 and key == self.current_player_name:
                self.current_index = self.names_of_players_remaining.index(self.current_player_name)
        return new_array


def sort_invest_array(val):
    return val['money_invest']


def remove_all_players_with_same_investment(players_ordered_by_invest, value):
    new_array = []
    for player in players_ordered_by_invest:
        if player['money_invest'] != value:
            new_array.append(player)

    return new_array
