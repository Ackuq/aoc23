import re
from typing import List, Set

regex = r"Card\s+\d+: (.*) \| (.*)"


def get_winning_hand(row: str) -> Set[int]:
    match = re.match(regex, row)
    if match is None:
        return set()
    winners = set(
        int(number) for number in match.group(1).strip().split(" ") if number != ""
    )
    hand = set(
        int(number) for number in match.group(2).strip().split(" ") if number != ""
    )
    return hand.intersection(winners)


def part1(input: List[str]) -> None:
    result = 0
    for row in input:
        winning_hand = get_winning_hand(row)
        if len(winning_hand) > 0:
            result += 2 ** (len(winning_hand) - 1)

    print(f"Part 1: {result}")


def part2(input: List[str]) -> None:
    scratch_boards = {index: 1 for index, _ in enumerate(input)}

    for index, row in enumerate(input):
        multiply = scratch_boards[index]
        winning_hand = get_winning_hand(row)

        for number in range(index + 1, index + len(winning_hand) + 1):
            scratch_boards[number] += multiply

    result = sum(scratch_boards.values())
    print(f"Part 2: {result}")


def main(input: List[str]) -> None:
    part1(input)
    part2(input)
