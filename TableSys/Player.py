from .PlayerHand import PlayerHand
from TableSys.FinanticalSys.PlayerFinancialSystem import PlayerFinancialSystem
from Enums import Status


class Player:
    def __init__(self, name, cash):
        self.bank_account = PlayerFinancialSystem(cash)
        self.name = name
        self.hand = PlayerHand()
        self.status = Status.WAIT_FOR_TURN.value
