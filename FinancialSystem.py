class FinancialSystem:

    def __init__(self, stating_amount):
        self.total_cash = stating_amount
        self.max_bet = stating_amount
        self.round_invest = 0  # after each card
        self.mini_game_invest = 0  # sum after each card

    def raise_bet(self, amount):
        if amount <= self.max_bet:  # TODO maybe move it to the location the player send amount
            self.max_bet -= amount
            self.round_invest = 0

    def call(self, bet_to_call):
        if bet_to_call > self.max_bet:
            self.round_invest += self.max_bet
            self.max_bet = 0

        else:
            self.round_invest += bet_to_call
            self.max_bet -= bet_to_call

    def fold(self):
        self.total_cash -= self.mini_game_invest
        self.mini_game_invest = 0
        self.round_invest = 0
        self.max_bet = self.total_cash

    def new_round(self):
        self.mini_game_invest += self.round_invest
        self.round_invest = 0

    def won_mini_game_update(self, cash):
        self.total_cash += cash
        self.max_bet = self.total_cash
        self.round_invest = 0  # after each card
        self.mini_game_invest = 0  # sum after each card
