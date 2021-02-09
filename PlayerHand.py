from collections import defaultdict
from Enums import CardValue, HandStrength
import numpy as np
import itertools


class PlayerHand:
    def __init__(self):
        self.first = None
        self.second = None

    def calculate_strength(self, cards_on_the_table):
        strongest_hand_rank = 0
        for combination in itertools.combinations(cards_on_the_table, 3):
            hand = [self.first, self.second].append(combination)
            result = check_straight_flush(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
            result = check_four_of_a_kind(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
            result = check_full_house(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
            result = check_flush(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
            result = check_straight(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
            result = check_three_of_a_kind(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
            result = check_two_pairs(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
            result = check_one_pairs(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
            result = check_high_card(hand)
            if result[0] and strongest_hand_rank < result[1]:
                strongest_hand_rank = result[1]
        return strongest_hand_rank


def check_straight_flush(hand):
    result = check_straight(hand)
    if check_flush(hand) and result[0]:
        return [True, calculate_hand_rank(HandStrength.STRAIGHT_FLUSH,
                                          [result[1], result[1] - 1, result[1] - 2, result[1] - 3,
                                           result[1] - 4])]
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
                forth_of_a_kind_value = i
            if value_counts[i] == 1:
                high_card = i

        return [True, calculate_hand_rank(HandStrength.FOUR_OF_KIND, [
            forth_of_a_kind_value, forth_of_a_kind_value, forth_of_a_kind_value,
            forth_of_a_kind_value, high_card])]

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
        return [True, calculate_hand_rank(HandStrength.FULL_HOUSE,
                                          three_value, three_value, three_value, pairs_value, pairs_value)]
    return False


def check_flush(hand):
    symbol = [i.symbol for i in hand]
    if len(set(symbol)) == 1:
        values = [i.value for i in hand]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        rank_values = [CardValue[i] for i in values]

        return [True, calculate_hand_rank(HandStrength.FLUSH,
                                          [max(rank_values), max(rank_values) - 1, max(rank_values) - 2,
                                           max(rank_values) - 3, max(rank_values) - 4])]
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
            return [True, calculate_hand_rank(HandStrength.STRAIGHT,
                                              [max(rank_values), max(rank_values) - 1, max(rank_values) - 2,
                                               max(rank_values) - 3, max(rank_values) - 4])]
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
            if value_counts[i] == 1 and i != second_card:
                first_card = i
            if value_counts[i] == 1 and i != first_card:
                second_card = i
        if first_card > second_card:
            return [True, calculate_hand_rank(HandStrength.THREE_OF_KIND,
                                              [three_value, three_value, three_value, first_card, second_card])]
        else:
            return [True, three_value, calculate_hand_rank(HandStrength.THREE_OF_KIND,
                                                           [three_value, three_value, three_value, second_card,
                                                            first_card])]

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
            if value_counts[i] == 1:
                high_card = i
        if first_pair_value > second_pair_value:
            return [True, calculate_hand_rank(HandStrength.TWO_PAIRS,
                                              [first_pair_value, first_pair_value, second_pair_value, second_pair_value,
                                               high_card])]
        else:
            return [True, calculate_hand_rank(HandStrength.TWO_PAIRS,
                                              [second_pair_value, second_pair_value, first_pair_value, first_pair_value,
                                               high_card])]
    return False


def check_one_pairs(hand):
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    free_cards = []
    if 2 in value_counts.values():
        for i in len(value_counts):
            if value_counts[i] == 2:
                pairs_value = i
            if value_counts[i] == 1:
                free_cards.append(i)
        return [True, calculate_hand_rank(HandStrength.PAIR,
                                          np.concatenate([pairs_value, pairs_value], free_cards.sort(reverse=True)))
                ]
    return False


def check_high_card(hand):
    high_card = 0
    values = [i.value for i in hand]
    value_counts = defaultdict(lambda: 0)
    free_cards = []
    for v in values:
        value_counts[v] += 1
        for i in len(value_counts):
            if value_counts[i] == 1:
                free_cards.append(i)
    return [True, calculate_hand_rank(HandStrength.HIGH_CARD, free_cards.sort(reverse=True))]


def calculate_hand_rank(strength, hand):
    return 10000000000 * strength + 100000000 * hand[0] + 1000000 * hand[1] + 10000 + hand[2] + 100 + hand[3] + 1 + \
           hand[4]
