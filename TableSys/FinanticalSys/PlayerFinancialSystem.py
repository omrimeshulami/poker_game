class PlayerFinancialSystem:

    def __init__(self, stating_amount):
        self.total_cash = stating_amount
        self.max_bet_allowed = stating_amount
        self.round_investment = 0  # after each card
        self.mini_game_investment = 0  # sum after each card
        self.mini_game_eared = 0

    def raise_bet(self, amount):
        amount = int(amount)
        if amount <= self.max_bet_allowed:
            self.max_bet_allowed -= amount
            self.round_investment += amount
            self.mini_game_investment += amount

    def need_all_in(self, bet_to_call):
        print(bet_to_call)
        return bet_to_call >= self.max_bet_allowed + self.round_investment

    def call(self, bet_to_call):
        if bet_to_call > self.max_bet_allowed:
            self.round_investment += self.max_bet_allowed
            self.mini_game_investment += self.max_bet_allowed
            self.max_bet_allowed = 0

        else:
            self.round_investment += bet_to_call
            self.mini_game_investment += bet_to_call
            self.max_bet_allowed -= bet_to_call

    def after_game_update(self):
        self.total_cash -= self.mini_game_investment
        self.max_bet_allowed = self.total_cash
        self.round_investment = 0  # after each card
        self.mini_game_investment = 0  # sum after each card
        self.mini_game_eared = 0

    def new_round(self):
        self.round_investment = 0

    def won_game_update(self, cash):
        self.total_cash -= self.mini_game_investment
        self.total_cash += cash
        self.max_bet_allowed = self.total_cash
        self.round_investment = 0  # after each card
        self.mini_game_investment = 0  # sum after each card
        self.mini_game_eared += cash
