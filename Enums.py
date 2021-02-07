from enum import Enum


class Symbol(Enum):
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    CLUBS = 4


class CardValue(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Status(Enum):
    RAISED = 'RAISED'
    CALLED = 'CALLED'
    FOLDED = 'FOLDED'
    CHECKED = "CHECKED"
    WAIT_FOR_TURN = 'WAIT_FOR_TURN'
    ALL_IN = "ALL_IN"

class TableStatus(Enum):
    NOT_READY = 'NOT_READY'
    READY = 'READY  '


class HandStrength(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FlUSH = 10
