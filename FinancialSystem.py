class FinancialSystem:

    def __init__(self, stating_amount):
        self.total_cash = stating_amount
        self.max_bet = stating_amount
        self.round_invested = 0  # after each card
        self.mini_game_invested = 0  # sum after each card
        self.all_in_by_others = 0
        self.mini_game_eared = 0
    def raise_bet(self, amount):
        amount = int(amount)
        if amount <= self.max_bet:
            self.max_bet -= amount
            self.round_invested += amount
            self.mini_game_invested += amount

    def need_all_in(self, bet_to_call):
        return bet_to_call >= self.max_bet+self.round_invested

    def call(self, bet_to_call):
        if bet_to_call > self.max_bet:
            self.round_invested += self.max_bet
            self.mini_game_invested += self.max_bet
            self.max_bet = 0

        else:
            self.round_invested += bet_to_call
            self.mini_game_invested += bet_to_call

            self.max_bet -= bet_to_call

    # def all_in_invested_by_others(self, money):
    #     if self.all_in_by_others == self.mini_game_invested:
    #         return 0
    #     elif self.all_in_by_others + money <= self.mini_game_invested:
    #         self.all_in_by_others += money
    #         return money
    #     else:
    #         val = self.mini_game_invested - self.all_in_by_others
    #         self.all_in_by_others = self.mini_game_invested
    #         return val

    def lost_game_update(self):
        self.total_cash -= self.mini_game_invested
        self.max_bet = self.total_cash
        self.round_invested = 0  # after each card
        self.mini_game_invested = 0  # sum after each card
        self.mini_game_eared = 0
        self.mini_game_eared = 0

    def new_round(self):
        self.round_invested = 0

    def won_game_update(self, cash):
        self.total_cash -= self.mini_game_invested
        self.total_cash += cash
        self.max_bet = self.total_cash
        self.round_invested = 0  # after each card
        self.mini_game_invested = 0  # sum after each card
        self.mini_game_eared += cash