class Card:
    def __init__(self, value, symbol):
        self.symbol = symbol
        self.value = value

    def print_card(self):
        if self.value==14:
            return f'[A{self.symbol}]'
        elif self.value==13:
            return f'[K{self.symbol}]'
        elif self.value==12:
            return f'[Q{self.symbol}]'
        elif self.value==11:
            return f'[J{self.symbol}]'
        else:
            return f'[{self.value}{self.symbol}]'
