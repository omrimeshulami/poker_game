from collections import defaultdict
from Enums import HandStrength
import numpy as np
import itertools


class PlayerHand:
    def __init__(self):
        self.first = None
        self.second = None

    def calculate_strength(self, cards_on_the_table):
        strongest_hand_rank = 0
        for combination in itertools.combinations(cards_on_the_table, 3):
            hand = np.concatenate(([self.first, self.second], combination))
            if strongest_hand_rank < get_hand_combination_strength(hand):
                strongest_hand_rank = get_hand_combination_strength(hand)
        for combination in itertools.combinations(cards_on_the_table, 4):
            hand = np.concatenate(([self.second], combination))
            if strongest_hand_rank < get_hand_combination_strength(hand):
                strongest_hand_rank = get_hand_combination_strength(hand)
        if strongest_hand_rank < get_hand_combination_strength(cards_on_the_table):
            strongest_hand_rank = get_hand_combination_strength(cards_on_the_table)
        return strongest_hand_rank

    def print_hand(self):
        return f'{self.first.print_card()},{self.second.print_card()}'


def get_hand_combination_strength(hand):
    strongest_hand_rank = 0
    hand_values = []
    for i in hand:
        hand_values.append(i.value)
    hand_symbols = []
    for i in hand:
        hand_symbols.append(i.symbol)
    result = check_straight_flush(hand_values, hand_symbols)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]
    result = check_four_of_a_kind(hand_values)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]

    result = check_full_house(hand_values)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]

    result = check_flush(hand_values, hand_symbols)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]

    result = check_straight(hand_values)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]

    result = check_three_of_a_kind(hand_values)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]

    result = check_two_pairs(hand_values)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]
    result = check_one_pairs(hand_values)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]
    result = check_high_card(hand_values)
    if result[0] and strongest_hand_rank < result[1]:
        return result[1]


def check_straight_flush(hand_values, hand_symbols):
    result = check_straight(hand_values)
    result1 = check_flush(hand_values, hand_symbols)
    if result1[0] and result[0]:
        hand_values = np.sort(hand_values)
        reverse_array = hand_values[::-1]
        return [True, calculate_hand_rank(HandStrength.STRAIGHT_FLUSH, reverse_array)]
    else:
        return [False]


def check_four_of_a_kind(hand_values):
    value_counts = defaultdict(lambda: 0)
    for v in hand_values:
        value_counts[v] += 1

    if sorted(value_counts.values()) == [1, 4]:
        for i in value_counts:
            if value_counts[i] == 4:
                forth_of_a_kind_value = i
            if value_counts[i] == 1:
                high_card = i
        #   print(
        #      f"full house hand send to calc: {[forth_of_a_kind_value, forth_of_a_kind_value, forth_of_a_kind_value, forth_of_a_kind_value, high_card]}")

        return [True, calculate_hand_rank(HandStrength.FOUR_OF_KIND, [
            forth_of_a_kind_value, forth_of_a_kind_value, forth_of_a_kind_value,
            forth_of_a_kind_value, high_card])]

    return [False]


def check_full_house(hand_values):
    value_counts = defaultdict(lambda: 0)
    for v in hand_values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [2, 3]:
        for i in value_counts:
            if value_counts[i] == 2:
                pairs_value = i
            if value_counts[i] == 3:
                three_value = i
        #   print(f"full house hand send to calc: {[three_value, three_value, three_value, pairs_value, pairs_value]}")

        return [True, calculate_hand_rank(HandStrength.FULL_HOUSE,
                                          [three_value, three_value, three_value, pairs_value, pairs_value])]
    return [False]


def check_flush(hand_values, hand_symbols):
    if len(set(hand_symbols)) == 1:
        hand_values = np.sort(hand_values)
        reverse_array = hand_values[::-1]
        return [True, calculate_hand_rank(HandStrength.FLUSH, reverse_array)]
    else:
        return [False]


def check_straight(hand_values):
    value_counts = defaultdict(lambda: 0)
    for v in hand_values:
        value_counts[v] += 1
    value_range = max(hand_values) - min(hand_values)
    if len(set(value_counts.values())) == 1 and (value_range == 4):
        hand_values = np.sort(hand_values)
        reverse_array = hand_values[::-1]
        return [True, calculate_hand_rank(HandStrength.STRAIGHT, reverse_array)]
    else:
        # check straight with low Ace
        hand_values = np.sort(hand_values)
        reverse_array = hand_values[::-1]
        if (reverse_array == [14, 5, 4, 3, 2]).all():
            #     print(f"stright hand send to calc: {reverse_array}")

            return [True, calculate_hand_rank(HandStrength.STRAIGHT, reverse_array)]
        return [False]


def check_three_of_a_kind(hand_values):
    first_card = -1
    second_card = -2
    value_counts = defaultdict(lambda: 0)
    for v in hand_values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 1, 3]:
        for i in value_counts:
            if value_counts[i] == 3:
                three_value = i
            if value_counts[i] == 1 and i != second_card and first_card == -1:
                first_card = i
            if value_counts[i] == 1 and i != first_card and second_card == -2:
                second_card = i
        if first_card > second_card:
            #    print(
            #        f"three of kind hand send to calc: {[three_value, three_value, three_value, first_card, second_card]}")

            return [True, calculate_hand_rank(HandStrength.THREE_OF_KIND,
                                              [three_value, three_value, three_value, first_card, second_card])]
        else:
            #     print(
            #       f"three of kind hand send to calc: {[three_value, three_value, three_value, second_card, first_card]}")

            return [True, three_value, calculate_hand_rank(HandStrength.THREE_OF_KIND,
                                                           [three_value, three_value, three_value, second_card,
                                                            first_card])]

    return [False]


def check_two_pairs(hand_values):
    first_pair_value = -1
    second_pair_value = -2
    value_counts = defaultdict(lambda: 0)
    for v in hand_values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 2, 2]:
        for i in value_counts:
            if value_counts[i] == 2 and i != second_pair_value and first_pair_value == -1:
                first_pair_value = i
            if value_counts[i] == 2 and i != first_pair_value and second_pair_value == -2:
                second_pair_value = i
            if value_counts[i] == 1:
                high_card = i
        if first_pair_value > second_pair_value:
            #  print(
            #      f"two pair hand send to calc: {[first_pair_value, first_pair_value, second_pair_value, second_pair_value, high_card]}")

            return [True, calculate_hand_rank(HandStrength.TWO_PAIRS,
                                              [first_pair_value, first_pair_value, second_pair_value, second_pair_value,
                                               high_card])]
        else:
            #    print(
            #          f"two pair hand send to calc: {[second_pair_value, second_pair_value, first_pair_value, first_pair_value, high_card]}")

            return [True, calculate_hand_rank(HandStrength.TWO_PAIRS,
                                              [second_pair_value, second_pair_value, first_pair_value, first_pair_value,
                                               high_card])]
    return [False]


def check_one_pairs(hand_values):
    value_counts = defaultdict(lambda: 0)
    for v in hand_values:
        value_counts[v] += 1
    free_cards = []
    if 2 in value_counts.values():
        for i in value_counts:
            if value_counts[i] == 2:
                pairs_value = i
            if value_counts[i] == 1:
                free_cards.append(i)
        free_cards = np.sort(free_cards)
        reverse_array = free_cards[::-1]
        hand = np.concatenate(([pairs_value, pairs_value], reverse_array))
        #  print(f"pair hand send to calc: {hand}")

        rank = calculate_hand_rank(HandStrength.PAIR, hand)
        return [True, rank]
    return [False]


def check_high_card(hand_values):
    hand_values = np.sort(hand_values)
    reverse_array = hand_values[::-1]
    # print(f"high card hand send to calc: {reverse_array}")
    return [True, calculate_hand_rank(HandStrength.HIGH_CARD, reverse_array)]


def calculate_hand_rank(strength, hand):
    rank = 10000000000 * strength.value + \
           100000000 * hand[0] + \
           1000000 * hand[1] + \
           10000 * hand[2] + \
           100 * hand[3] + \
           1 * hand[4]
    return rank
