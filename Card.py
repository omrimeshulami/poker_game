class Card:
    def __init__(self, value, symbol):
        self.symbol = symbol
        self.value = value

    def print_card(self):
        return f'Vlaue: {self.value} , Symbol: {self.symbol}'
