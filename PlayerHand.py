from collections import defaultdict
from Enums import CardValue,HandStrength


class PlayerHand:
    def __init__(self):
        self.first = None
        self.second = None

    def calculate_strength(self, other_three_cards):  # TODO add each method all the hand info
        hand = [self.first, self.second].append(other_three_cards)
        result = check_straight_flush(hand)
        if result[0]:
            return [HandStrength.STRAIGHT_FLUSH, result[1]]
        result = check_four_of_a_kind(hand)
        if result[0]:
            return [HandStrength.FOUR_OF_KIND, result[1]]
        result = check_full_house(hand)
        if result[0]:
            return [HandStrength.FULL_HOUSE, result[1], result[2]]
        if check_flush(hand):
            return [HandStrength.FLUSH]
        result = check_straight(hand)
        if result[0]:
            return [HandStrength.STRAIGHT, result[1]]
        result = check_three_of_a_kind(hand)
        if result[0]:
            return [HandStrength.THREE_OF_KIND, result[1]]
        result = check_two_pairs(hand)
        if result[0]:
            return [HandStrength.TWO_PAIRS, result[1], result[2]]
        result = check_one_pairs(hand)
        if result[0]:
            return [HandStrength.PAIR, result[1]]
        result = check_high_card(hand)
        if result[0]:
            return [HandStrength.HIGH_CARD, result[1]]


def check_straight_flush(hand):
    result = check_straight(hand)
    if check_flush(hand) and result[0]:
        return [True, result[1]]
    else:
        return False


def check_four_of_a_kind(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1

    if sorted(value_counts.values()) == [1, 4]:
        for i in len(value_counts):
            if value_counts[i] == 4:
                return [True, i]
    return False


def check_full_house(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [2, 3]:
        for i in len(value_counts):
            if value_counts[i] == 2:
                pairs_value = i
            if value_counts[i] == 3:
                three_value = i
        return [True, three_value, pairs_value]
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
    rank_values = [CardValue[i] for i in values]
    value_range = max(rank_values) - min(rank_values)
    if len(set(value_counts.values())) == 1 and (value_range == 4):
        return True
    else:
        # check straight with low Ace
        if set(values) == set(["A", "TWO", "TREE", "FOUR", "FIVE"]):
            return [True, max(rank_values)]
        return False


def check_three_of_a_kind(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 1, 3]:
        for i in len(value_counts):
            if value_counts[i] == 3:
                three_value = i
        return [True, three_value]
    return False


def check_two_pairs(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 2, 2]:
        for i in len(value_counts):
            if value_counts[i] == 2 and i != second_pair_value:
                first_pair_value = i
            if value_counts[i] == 2 and i != first_pair_value:
                second_pair_value = i

        if first_pair_value > second_pair_value:
            return [True, first_pair_value, second_pair_value]
        else:
            return [True, second_pair_value, first_pair_value]
    return False


def check_one_pairs(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if 2 in value_counts.values():
        for i in len(value_counts):
            if value_counts[i] == 2:
                pairs_value = i

                return [True, pairs_value]
            return False


def check_high_card(hand):
    high_card = 0
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if 2 in value_counts.values():
        for i in len(value_counts):
            if value_counts[i] == 1 and high_card < i:
                high_card = i
                return [True, high_card]
            return False
