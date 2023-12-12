import re
from copy import deepcopy
from typing import List, Tuple

import tqdm

Input = List[Tuple[List[str], List[int]]]


def parse_input(lines: List[str]) -> Input:
    input = []
    for line in lines:
        conditions_str, sizes_str = line.strip().split(" ")
        conditions = list(conditions_str)
        sizes = [int(size) for size in sizes_str.split(",")]
        input.append((conditions, sizes))

    return input


def part1(input: Input) -> None:
    def generate_possibilities(conditions: List[str]) -> List[List[str]]:
        possibilities: List[List[str]] = []
        for condition in conditions:
            if condition == "?":
                left = deepcopy(possibilities) if len(possibilities) > 0 else [[]]
                right = deepcopy(possibilities) if len(possibilities) > 0 else [[]]
                for possibility in left:
                    possibility.append("#")
                for possibility in right:
                    possibility.append(".")
                possibilities = left + right
            if condition == "#":
                if len(possibilities) == 0:
                    possibilities = [["#"]]
                    continue
                for possibility in possibilities:
                    possibility.append("#")
            if condition == ".":
                if len(possibilities) == 0:
                    possibilities = [["."]]
                    continue
                for possibility in possibilities:
                    possibility.append(".")
        return possibilities

    def generate_regex(sizes: List[int]) -> str:
        regex = r"^\.*"
        for size in sizes[:-1]:
            regex += f"#{{{size}}}" + r"\.+"
        regex += f"#{{{sizes[-1]}}}" + r"\.*$"
        return regex

    result = 0
    for conditions, sizes in tqdm.tqdm(input):
        regex = generate_regex(sizes)
        possibilities = generate_possibilities(conditions)
        for possibility in possibilities:
            match = re.match(regex, "".join(possibility))
            if match is not None:
                result += 1

    print("Part 1:", result)


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
