from functools import cmp_to_key
from typing import Dict, List, Tuple

Hand = Dict[str, int]
Player = Tuple[Hand, List[str], int]
Input = List[Player]


def parse_hand(hand: str) -> Hand:
    hands: Hand = {}
    for card in hand:
        if card in hands:
            hands[card] += 1
        else:
            hands[card] = 1
    return hands


def parse_input(lines: List[str]) -> Input:
    input: Input = []
    for line in lines:
        hand, rank = line.strip().split()
        input.append((parse_hand(hand), list(hand), int(rank)))
    return input


card_strengths = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def part1(input: Input) -> None:
    def is_pair(hand: Hand) -> bool:
        return 2 in hand.values() and len(hand) == 4

    def is_two_pair(hand: Hand) -> bool:
        return 2 in hand.values() and len(hand) == 3

    def is_full_house(hand: Hand) -> bool:
        return 2 in hand.values() and 3 in hand.values()

    def get_hand_value(hand: Hand) -> int:
        value = max(hand.values())
        if value == 5:
            # Five of a kind
            return 6
        if value == 4:
            # Four of a kind
            return 5
        if is_full_house(hand):
            # Full house
            return 4
        if value == 3:
            # Three of a kind
            return 3
        if is_two_pair(hand):
            return 2
        if is_pair(hand):
            return 1
        return 0

    def compare(player1: Player, player2: Player) -> int:
        max_pairs1 = get_hand_value(player1[0])
        max_pairs2 = get_hand_value(player2[0])
        if max_pairs1 > max_pairs2:
            # player 1 wins
            return 1
        elif max_pairs2 > max_pairs1:
            # player 2 wins
            return -1
        for card1, card2 in zip(player1[1], player2[1]):
            card1_strength = card_strengths.index(card1)
            card2_strength = card_strengths.index(card2)
            if card1_strength > card2_strength:
                # player 1 wins
                return 1
            elif card2_strength > card1_strength:
                # player 2 wins
                return -1
        return 0

    compare_key = cmp_to_key(compare)
    sorted_hands = sorted(input, key=compare_key)
    result = 0
    for i, hand in enumerate(sorted_hands):
        result += hand[2] * (i + 1)

    print("Part 1:", result)


card_strengths2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def part2(input: Input) -> None:
    # TODO: Finish this
    def is_pair(hand: Hand) -> bool:
        return 2 in hand.values() and len(hand) == 4

    def is_two_pair(hand: Hand) -> bool:
        return 2 in hand.values() and len(hand) == 3

    def is_full_house(hand: Hand) -> bool:
        return 2 in hand.values() and 3 in hand.values()

    def get_hand_value(hand: Hand) -> int:
        value = max(hand.values())
        if value == 5 or value == 4:
            # Five of a kind
            return 6
        if value == 4:
            # Four of a kind
            return 5
        if is_full_house(hand):
            # Full house
            return 4
        if value == 3:
            # Three of a kind
            return 3
        if is_two_pair(hand):
            return 2
        if is_pair(hand):
            return 1
        return 0

    def compare(player1: Player, player2: Player) -> int:
        max_pairs1 = get_hand_value(player1[0])
        max_pairs2 = get_hand_value(player2[0])
        if max_pairs1 > max_pairs2:
            # player 1 wins
            return 1
        elif max_pairs2 > max_pairs1:
            # player 2 wins
            return -1
        for card1, card2 in zip(player1[1], player2[1]):
            card1_strength = card_strengths2.index(card1)
            card2_strength = card_strengths2.index(card2)
            if card1_strength > card2_strength:
                # player 1 wins
                return 1
            elif card2_strength > card1_strength:
                # player 2 wins
                return -1
        return 0

    compare_key = cmp_to_key(compare)
    sorted_hands = sorted(input, key=compare_key)
    result = 0
    for i, hand in enumerate(sorted_hands):
        result += hand[2] * (i + 1)


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
