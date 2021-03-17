from collections import defaultdict
from Enums import HandStrength
import numpy as np
import itertools


class PlayerHand:
    def __init__(self):
        self.first = None
        self.second = None

    def print_hand(self):
        return f'{self.first.print_card()},{self.second.print_card()}'

    def rank_score(self, cards_on_the_table):
        strongest_hand_rank = {'rank_score': 0, 'hand': []}
        for combination in itertools.combinations(cards_on_the_table, 3):
            hand = np.concatenate(([self.first, self.second], combination))  # player cards + 3 on the table
            if strongest_hand_rank['rank_score'] < get_hand_combination_strength(hand)['rank_score']:
                strongest_hand_rank = get_hand_combination_strength(hand)
        for combination in itertools.combinations(cards_on_the_table, 4):
            hand_with_first_card = np.concatenate(([self.first], combination))  # player  card + 4 on the table
            hand_with_second_card = np.concatenate(([self.second], combination))
            if strongest_hand_rank['rank_score'] < get_hand_combination_strength(hand_with_first_card)['rank_score']:
                strongest_hand_rank = get_hand_combination_strength(hand_with_first_card)
            if strongest_hand_rank['rank_score'] < get_hand_combination_strength(hand_with_second_card)['rank_score']:
                strongest_hand_rank = get_hand_combination_strength(hand_with_second_card)
        if strongest_hand_rank['rank_score'] < get_hand_combination_strength(cards_on_the_table)['rank_score']:
            strongest_hand_rank = get_hand_combination_strength(cards_on_the_table)  # 5 on the table
        return strongest_hand_rank


def get_hand_combination_strength(hand):
    strongest_hand_rank = 0
    hand_values = [i.value for i in hand]
    hand_symbols = [i.symbol for i in hand]
    verification_and_rank_score = check_straight_flush(hand_values, hand_symbols)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'Straight Flush', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}

    verification_and_rank_score = check_four_of_a_kind(hand_values)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'Four Of A Kind', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}

    verification_and_rank_score = check_full_house(hand_values)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'Full House', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}

    verification_and_rank_score = check_flush(hand_values, hand_symbols)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'Flush', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}

    verification_and_rank_score = check_straight(hand_values)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'Straight', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}

    verification_and_rank_score = check_three_of_a_kind(hand_values)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'Three Of A kind', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}

    verification_and_rank_score = check_two_pairs(hand_values)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'Two Pairs', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}

    verification_and_rank_score = check_one_pairs(hand_values)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'One Pair', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}

    verification_and_rank_score = check_high_card(hand_values)
    if verification_and_rank_score['verification'] and strongest_hand_rank < verification_and_rank_score['rank_score']:
        return {'rank_name': 'High Card', 'rank_score': verification_and_rank_score['rank_score'], 'hand': hand}


def check_straight_flush(hand_values, hand_symbols):
    verification_and_rank_straight = check_straight(hand_values)
    verification_and_rank_straight_flush = check_flush(hand_values, hand_symbols)
    if verification_and_rank_straight['verification'] and verification_and_rank_straight_flush['verification']:
        reversed_array = np.sort(hand_values)[::-1]
        rank_score = calculate_hand_rank(HandStrength.STRAIGHT_FLUSH, reversed_array)
        return {'verification': True, 'rank_score': rank_score}
    else:
        return {'verification': False, 'rank_score': 0}


def check_four_of_a_kind(hand_values):
    value_counts = defaultdict(lambda: 0)
    value_counts = {i: value_counts[i] + 1 for i in hand_values}

    if sorted(value_counts.values()) == [1, 4]:
        forth_of_a_kind_value = [value_count for value_count in value_counts if value_counts[value_count] == 4][0]
        high_card_value = [value_count for value_count in value_counts if value_counts[value_count] == 4][0]
        hand = [forth_of_a_kind_value, forth_of_a_kind_value, forth_of_a_kind_value, forth_of_a_kind_value,
                high_card_value]
        rank_score = calculate_hand_rank(HandStrength.FOUR_OF_KIND, hand)
        return {'verification': True, 'rank_score': rank_score}

    return {'verification': False, 'rank_score': 0}


def check_full_house(hand_values):
    value_counts = defaultdict(lambda: 0)
    value_counts = {i: value_counts[i] + 1 for i in hand_values}

    if sorted(value_counts.values()) == [2, 3]:
        three_value = [value_count for value_count in value_counts if value_counts[value_count] == 3][0]
        pairs_value = [value_count for value_count in value_counts if value_counts[value_count] == 2][0]
        hand = [three_value, three_value, three_value, pairs_value, pairs_value]
        rank_score = calculate_hand_rank(HandStrength.FULL_HOUSE, hand)
        return {'verification': True, 'rank_score': rank_score}
    return {'verification': False, 'rank_score': 0}


def check_flush(hand_values, hand_symbols):
    if len(set(hand_symbols)) == 1:
        reversed_array = np.sort(hand_values)[::-1]
        rank_score = calculate_hand_rank(HandStrength.FLUSH, reversed_array)
        return {'verification': True, 'rank_score': rank_score}
    else:
        return {'verification': False, 'rank_score': 0}


def check_straight(hand_values):
    value_counts = defaultdict(lambda: 0)
    value_counts = {i: value_counts[i] + 1 for i in hand_values}
    value_range = max(hand_values) - min(hand_values)

    if len(set(value_counts.values())) == 1 and (value_range == 4):
        reversed_array = np.sort(hand_values)[::-1]
        rank_score = calculate_hand_rank(HandStrength.STRAIGHT, reversed_array)
        return {'verification': True, 'rank_score': rank_score}
    else:
        # check straight with low Ace
        reversed_array = np.sort(hand_values)[::-1]
        is_low_straight = (reversed_array == [14, 5, 4, 3, 2]).all()
        if is_low_straight:
            rank_score = calculate_hand_rank(HandStrength.STRAIGHT, reversed_array)
            return {'verification': True, 'rank_score': rank_score}
        return {'verification': False, 'rank_score': 0}


def check_three_of_a_kind(hand_values):
    value_counts = defaultdict(lambda: 0)
    value_counts = {i: value_counts[i] + 1 for i in hand_values}

    if sorted(value_counts.values()) == [1, 1, 3]:
        three_value = [value_count for value_count in value_counts if value_counts[value_count] == 3][0]
        separated_cards_value = [value_count for value_count in value_counts if value_counts[value_count] == 1]
        separated_cards_value = np.sort(separated_cards_value)
        hand = [three_value, three_value, three_value, separated_cards_value[1], separated_cards_value[0]]
        rank_score = calculate_hand_rank(HandStrength.THREE_OF_KIND, hand)
        return {'verification': True, 'rank_score': rank_score}
    return {'verification': False, 'rank_score': 0}


def check_two_pairs(hand_values):
    value_counts = defaultdict(lambda: 0)
    value_counts = {i: value_counts[i] + 1 for i in hand_values}

    if sorted(value_counts.values()) == [1, 2, 2]:
        pairs_values = [value_count for value_count in value_counts if value_counts[value_count] == 2]
        high_card_value = [value_count for value_count in value_counts if value_counts[value_count] == 1][0]
        pairs_values = np.sort(pairs_values)
        hand = [pairs_values[1], pairs_values[1], pairs_values[0], pairs_values[0], high_card_value]
        rank_score = calculate_hand_rank(HandStrength.TWO_PAIRS, hand)
        return {'verification': True, 'rank_score': rank_score}
    return {'verification': False, 'rank_score': 0}


def check_one_pairs(hand_values):
    value_counts = defaultdict(lambda: 0)
    value_counts = {i: value_counts[i] + 1 for i in hand_values}

    if 2 in value_counts.values():
        pair_value = [value_count for value_count in value_counts if value_counts[value_count] == 2][0]
        separated_cards_value = [value_count for value_count in value_counts if value_counts[value_count] == 1][0]
        separated_cards_value_reversed = np.sort(separated_cards_value)[::-1]
        hand = np.concatenate(([pair_value, pair_value], separated_cards_value_reversed))
        rank_score = calculate_hand_rank(HandStrength.PAIR, hand)
        return {'verification': True, 'rank_score': rank_score}
    return {'verification': False, 'rank_score': 0}


def check_high_card(hand_values):
    hand_values = np.sort(hand_values)
    reverse_array = hand_values[::-1]
    rank_score = calculate_hand_rank(HandStrength.HIGH_CARD, reverse_array)
    return {'verification': True, 'rank_score': rank_score}


def calculate_hand_rank(strength, hand):
    rank = 10000000000 * strength.value + \
           100000000 * hand[0] + \
           1000000 * hand[1] + \
           10000 * hand[2] + \
           100 * hand[3] + \
           1 * hand[4]
    return rank
