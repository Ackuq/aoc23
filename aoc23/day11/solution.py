from itertools import combinations
from typing import List


def debug_print(input: List[str]) -> None:
    for row in input:
        print(row)


def part1(input: List[str]) -> None:
    def expand(input: List[str]) -> List[str]:
        new_input = []
        for row in input:
            new_input.append(row)
            if all([c == "." for c in row]):
                new_input.append(row)

        length = len(new_input[0])
        col = 0
        while col < length:
            if all([row[col] == "." for row in new_input]):
                for i, row in enumerate(new_input):
                    new_input[i] = row[:col] + "." + row[col:]
                length += 1
                col += 1
            col += 1

        return new_input

    expanded = expand(input)
    galaxies = [
        (x, y)
        for y, row in enumerate(expanded)
        for x, column in enumerate(row)
        if column == "#"
    ]
    # Get all pairs
    pairs = list(combinations(galaxies, 2))
    result = 0

    for (x1, y1), (x2, y2) in pairs:
        shortest_path = abs(x1 - x2) + abs(y1 - y2)
        result += shortest_path

    print("Part 1:", result)


def main(input: List[str]) -> None:
    stripped_input = [line.strip() for line in input]
    part1(stripped_input)
