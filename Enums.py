from enum import Enum


class Symbol(Enum):
    DIAMONDS = "♦"
    HEARTS = "♥"
    SPADES = "♣"
    CLUBS = "♠"


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
    DEALER = 'DEALER'
    SMALL_BLIND = 'SMALL_BLIND'
    BIG_BLIND = 'BIG_BLIND'
    WAIT_FOR_TURN = 'WAIT_FOR_TURN'
    RAISE_ALL_IN = "RAISE_ALL_IN"
    CALL_ALL_IN = "CALL_ALL_IN"
    ALL_IN = "ALL_IN"


class TableStatus(Enum):
    WAIT_FOR_PLAYERS = 'WAIT_FOR_PLAYERS'
    RUNNING = 'RUNNING'
    STARTING_NEW_ROUND = 'STARTING_NEW_ROUND'
    GAME_FINISHED = 'GAME_FINISHED'
    TABLE_FINISHED = 'TABLE_FINISHED'
    STARTING_NEW_GAME = 'STARTING_NEW_GAME'


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


class TestMode(Enum):
    MANUALLY = 'MANUALLY'
    AUTOMATICALLY = 'AUTOMATICALLY'


class UserStatus(Enum):
   ONLINE = 'ONLINE'
   OFFLINE = 'OFFLINE'
   PLAYING = 'PLAYING'