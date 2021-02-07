import Deck
import random
from Enums import Status


# TODO compare same lvl of hands,action player raised, and the todos below that most important

class Table:
    def __init__(self, players, small_blind_value, big_blind_value):
        self.pot = 0
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

    def player_action(self, action, name):
        actions_parts = action.split()
        if actions_parts[0].lower() == "fold":
            self.players[name].status = Status.FOLDED       #TODO "FOLD" LOOKS LIKE ITS FINISHED
            self.players_remaining.pop(name)
            self.players[name].bank_account.fold()
            if len(self.players_remaining) == 1:
                self.end_mini_game()
            else:
                self.complete_player_turn()

        elif actions_parts[0].lower() == "call":        #TODO "CALL" LOOKS LIKE ITS FINISHED
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
            self.players[name].status = Status.RAISED                   #TODO "FOLD" LOOKS LIKE ITS FINISHED
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
    #TODO FINISHED
    def update_players_bank_after_mini_game(self, name):
        for p in self.players:
            p.bank_accout.fold()
        self.players[name].back_account.won_mini_game_update(self.pot)


    #TODO need to split the player to gruops by how mcuh they invested in the pot then check who won in each gruop
    #TODO then start from the top down to see how to split the money (split to methods)
    def winner_name(self):
        if len(self.cards_on_the_table) == 3:
            all_player_hand_strength = [p.hand.calculate_strength() for p in self.players]
            sorter_ = lambda x: (x[0])  # lambda to sort by
            sorted_l = sorted(all_player_hand_strength, key=sorter_)
            while sorted_l[0][0] != sorted_l[len(sorted_l) - 1]:
                sorted_l = sorted_l[1:]
            if len(sorted_l) == 1:
                return sorted_l[0]

    # TODO FINISHED
    def switch_to_next_player(self):
        while True:
            if self.players_remaining.index(self.current_player) + 1 <= len(self.players_remaining) - 1:
                self.current_player = self.players_remaining[
                    self.players_remaining.index(self.current_player) + 1]
            else:
                self.current_player = self.players_remaining[0]
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
        winner = self.winner_name()
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
