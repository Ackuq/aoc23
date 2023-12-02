import functools
import re
from typing import Dict, List, Literal

Cube = Literal["red"] | Literal["blue"] | Literal["green"]
cubes: List[Cube] = ["red", "blue", "green"]
Bag = Dict[Cube, int]
Game = List[Bag]

initial: Bag = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def part1(games: List[Game]) -> int:
    def is_valid_set(bag: Bag) -> bool:
        return all(bag[cube] <= initial[cube] for cube in bag)

    def is_valid_game(game: Game) -> bool:
        return all(is_valid_set(set) for set in game)

    result = sum([index + 1 for index, game in enumerate(games) if is_valid_game(game)])

    print(f"Part 1: {result}")


def part2(games: List[Game]) -> int:
    def reduce(prev: Bag, bag: Bag) -> Bag:
        return {
            "red": max(prev["red"], bag["red"]),
            "green": max(prev["green"], bag["green"]),
            "blue": max(prev["blue"], bag["blue"]),
        }

    def get_min_bag_sum(game: Game) -> int:
        min_bag = functools.reduce(
            reduce,
            game,
            {
                "red": 0,
                "green": 0,
                "blue": 0,
            },
        )
        return min_bag["blue"] * min_bag["green"] * min_bag["red"]

    result = sum([get_min_bag_sum(game) for game in games])

    print(f"Part 2: {result}")


def main(input: List[str]) -> None:
    games = parse_input(input)
    part1(games)
    part2(games)


def parse_input(input: List[str]) -> List[Game]:
    def create_set(set: str) -> Bag:
        bag: Bag = {}
        for cube in cubes:
            regex = r"(\d+) " + cube
            match = re.search(regex, set)
            if match is None:
                bag[cube] = 0
                continue
            bag[cube] = int(match.group(1))
        return bag

    def create_game(game: str) -> Game:
        sets = game.split(";")
        return [create_set(set) for set in sets]

    result: List[Game] = [create_game(game) for game in input]

    return result
