from copy import deepcopy
from typing import Dict, List, Tuple

Input = List[List[str]]
Coord = Tuple[int, int]


def parse_input(lines: List[str]) -> List[List[str]]:
    return [list(line.strip()) for line in lines]


def print_input(input: Input) -> None:
    print()
    for line in input:
        print("".join(line))


def move(coord: Coord, input: Input, delta_x: int, delta_y: int) -> Input:
    x, y = coord
    input[y][x] = "."
    next_x = x
    next_y = y
    while (
        (next_x + delta_x) < len(input)
        and (next_x + delta_x) >= 0
        and (next_y + delta_y) < len(input)
        and (next_y + delta_y) >= 0
        and input[next_y + delta_y][next_x + delta_x] == "."
    ):
        next_x += delta_x
        next_y += delta_y
    input[next_y][next_x] = "O"
    return input


def tilt_lever(input: Input, direction: int) -> Input:
    delta_x = [0, -1, 0, 1][direction]
    delta_y = [-1, 0, 1, 0][direction]
    # If moving from bottom, start from bottom
    y_range = range(len(input) - 1, -1, -1) if direction == 2 else range(len(input))
    # If moving from right, start from right
    x_range = (
        range(len(input[0]) - 1, -1, -1) if direction == 3 else range(len(input[0]))
    )

    for y in y_range:
        line = input[y]
        for x in x_range:
            c = line[x]
            if c == "O":
                input = move((x, y), input, delta_x, delta_y)

    return input


def get_load(input: Input) -> int:
    load = 0
    for y, line in enumerate(input):
        for c in line:
            if c == "O":
                load += len(input) - y
    return load


def part1(input: Input) -> None:
    input = tilt_lever(deepcopy(input), 0)
    load = get_load(input)
    print(f"Part 1: {load}")


def part2(input: Input) -> None:
    cycles = 4_000_000_000
    cache: Dict[Tuple[str, int], Input] = {}
    cache_order: List[Tuple[str, int]] = []

    cycle_start = 0
    cycle_end = 0
    for i in range(cycles):
        direction = i % 4
        cache_key = ("".join(["".join(line) for line in input]), direction)
        if cache_key in cache:
            # Cycle detected, we can calculate the final load
            cycle_start = cache_order.index(cache_key)
            cycle_end = i
            break
        cache_order.append(cache_key)
        cache[cache_key] = deepcopy(input)
        input = tilt_lever(input, direction)

    # Get the length of the repeating cycle
    cycle_length = cycle_end - cycle_start
    # Get the offset where only the repeating cycle is left
    cycle_offset = cycles - cycle_start
    # Get the index of the repeating cycle
    cycle_index = cycle_offset % cycle_length
    # Get the cache key of the 4 billionth iteration
    cache_key = cache_order[cycle_start + cycle_index]

    load = get_load(cache[cache_key])
    print(f"Part 2: {load}")


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
