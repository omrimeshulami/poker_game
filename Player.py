import PlayerHand
import FinancialSystem
from Enums import Status


class Player:
    def __init__(self, name, cash):
        self.bank_account = FinancialSystem(cash)
        self.name = name
        self.hand = PlayerHand
        self.role = None
        self.status = Status.FOLD
