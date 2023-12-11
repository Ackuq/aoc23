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
            if all(c == "." for c in row):
                new_input.append(row)

        length = len(new_input[0])
        col = 0
        while col < length:
            if all(row[col] == "." for row in new_input):
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


def part2(input: List[str]) -> None:
    def get_expanded_rows(input: List[str]) -> List[int]:
        expanded_rows: List[int] = []
        for i, row in enumerate(input):
            if all(c == "." for c in row):
                expanded_rows.append(i)
        return expanded_rows

    def get_expanded_columns(input: List[str]) -> List[int]:
        expanded_columns: List[int] = []
        for col, _ in enumerate(input[0]):
            if all([row[col] == "." for row in input]):
                expanded_columns.append(col)
        return expanded_columns

    galaxies = [
        (x, y)
        for y, row in enumerate(input)
        for x, column in enumerate(row)
        if column == "#"
    ]

    expanded_rows = get_expanded_rows(input)
    expanded_columns = get_expanded_columns(input)

    # Get all pairs
    pairs = list(combinations(galaxies, 2))
    result = 0

    for (x1, y1), (x2, y2) in pairs:
        range_x = range(min(x1, x2), max(x1, x2) + 1)
        range_y = range(min(y1, y2), max(y1, y2) + 1)
        millions_to_pass = 0
        for y in expanded_rows:
            if y in range_y:
                millions_to_pass += 1
        for x in expanded_columns:
            if x in range_x:
                millions_to_pass += 1
        shortest_path = abs(x1 - x2) + abs(y1 - y2)
        result += shortest_path + millions_to_pass * 999_999

    print("Part 2:", result)


def main(input: List[str]) -> None:
    stripped_input = [line.strip() for line in input]
    part1(stripped_input)
    part2(stripped_input)
