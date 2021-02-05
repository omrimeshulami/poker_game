from collections import defaultdict
from Enums import CardValue

def check_straight_flush(hand):
    if check_flush(hand) and check_straight(hand):
        return True
    else:
        return False


def check_four_of_a_kind(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 4]:
        return True
    return False


def check_full_house(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [2, 3]:
        return True
    return False


def check_flush(hand):
    symbol = [i.symbol for i in hand]
    if len(set(symbol)) == 1:
        return True
    else:
        return False


def check_straight(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    rank_values = [card_order_dict[i] for i in values]
    value_range = max(rank_values) - min(rank_values)
    if len(set(value_counts.values())) == 1 and (value_range == 4):
        return True
    else:
        # check straight with low Ace
        if set(values) == set(["A", "2", "3", "4", "5"]):
            return True
        return False


def check_three_of_a_kind(hand):
    pass


def check_two_pairs(hand):
    pass


def check_one_pairs(hand):
    pass


class PlayerHand:
    def __init__(self):
        self.first = None
        self.second = None

    def calculate_strength(self, other_three_cards):
        hand = [self.first, self.second].append(other_three_cards)
        if check_straight_flush(hand):
            return 9
        if check_four_of_a_kind(hand):
            return 8
        if check_full_house(hand):
            return 7
        if check_flush(hand):
            return 6
        if check_straight(hand):
            return 5
        if check_three_of_a_kind(hand):
            return 4
        if check_two_pairs(hand):
            return 3
        if check_one_pairs(hand):
            return 2
        return 1
