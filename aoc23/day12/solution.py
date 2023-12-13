from functools import cache, reduce
from typing import List, Tuple

Input = List[Tuple[Tuple[str, ...], Tuple[int, ...]]]


def parse_input(lines: List[str]) -> Input:
    input = []
    for line in lines:
        conditions_str, sizes_str = line.strip().split(" ")
        conditions = tuple(conditions_str)
        sizes = tuple(int(size) for size in sizes_str.split(","))
        input.append((conditions, sizes))

    return input


@cache
def is_valid(rest: Tuple[str], sizes: Tuple[int]) -> int:
    # If we have no more conditions and no more sizes, we have a valid path
    if (len(rest) == 0 and len(sizes) == 0) or (
        # If we have no more sizes, we can only have dots and question marks
        len(sizes) == 0
        and all(c == "." or c == "?" for c in rest)
    ):
        return 1
    # If we have no more conditions or no more sizes, we have an invalid path
    if len(rest) == 0 or len(sizes) == 0:
        return 0
    current = rest[0]
    if current == "#":
        if (
            # The rest of the path must be at least as long as the current size
            len(rest) >= sizes[0]
            # We need a consecutive sequence of broken springs
            and all(c == "#" or c == "?" for c in rest[: sizes[0]])
            and (
                # If we have reached the end of the path, we have a valid path
                # Otherwise the next spring must be functional
                len(rest) == sizes[0]
                or rest[sizes[0]] == "."
                or rest[sizes[0]] == "?"
            )
        ):
            return is_valid(rest[sizes[0] + 1 :], sizes[1:])
        return 0
    if current == ".":
        return is_valid(rest[1:], sizes)
    if current == "?":
        # We can either have a broken spring or a functional spring
        return is_valid(("#",) + rest[1:], sizes) + is_valid((".",) + rest[1:], sizes)

    raise Exception("Invalid input")


def part1(input: Input) -> None:
    result = 0
    for conditions, sizes in input:
        result += is_valid(conditions, sizes)
    print("Part 1:", result)


def part2(input: Input) -> None:
    result = 0
    for conditions, sizes in input:
        new_sizes = sizes * 5
        new_conditions = reduce(lambda a, b: a + ("?",) + b, (conditions,) * 5)
        result += is_valid(new_conditions, new_sizes)
    print("Part 2:", result)


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
