from .PlayerHand import PlayerHand
from .FinancialSystem import FinancialSystem
from Enums import Status


class Player:
    def __init__(self, name, cash):
        self.bank_account = FinancialSystem(cash)
        self.name = name
        self.hand = PlayerHand()
        self.status = Status.WAIT_FOR_TURN.value
