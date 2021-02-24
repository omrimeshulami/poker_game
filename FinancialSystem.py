class FinancialSystem:

    def __init__(self, stating_amount):
        self.total_cash = stating_amount
        self.max_bet = stating_amount
        self.round_invested = 0  # after each card
        self.mini_game_invested = 0  # sum after each card

    def raise_bet(self, amount):
        amount = int(amount)
        if amount <= self.max_bet:
            self.max_bet -= amount
            self.round_invested += amount
            self.mini_game_invested += amount

    def need_all_in(self, bet_to_call):
        return bet_to_call > self.max_bet

    def call(self, bet_to_call):
        if bet_to_call > self.max_bet:
            self.round_invested += self.max_bet
            self.mini_game_invested += self.max_bet
            self.max_bet = 0

        else:
            self.round_invested += bet_to_call
            self.mini_game_invested += bet_to_call

            self.max_bet -= bet_to_call

    def fold(self):
        self.total_cash -= self.mini_game_invested
        self.max_bet = self.total_cash
        self.round_invested = 0  # after each card
        self.mini_game_invested = 0  # sum after each card

    def new_mini_game(self):
        self.total_cash -= self.mini_game_invested
        self.max_bet = self.total_cash
        self.round_invested = 0  # after each card
        self.mini_game_invested = 0  # sum after each card

    def new_round(self):
        self.round_invested = 0

    def won_mini_game_update(self, cash):
        self.total_cash -= self.mini_game_invested
        self.total_cash += cash
        self.max_bet = self.total_cash
        self.round_invested = 0  # after each card
        self.mini_game_invested = 0  # sum after each card
