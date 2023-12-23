import sys
from typing import List, Literal, Set, Tuple, cast

# # = forest
# . = path
# ^ = up slope
# v = down slope
# < = left slope
# > = right slope
Cell = Literal["#", ".", "^", "v", "<", ">"]
Coord = Tuple[int, int]
Input = List[List[Cell]]


def parse_input(input: List[str]) -> Input:
    return [cast(List[Cell], list(line.strip())) for line in input]


directions = {(0, -1), (0, 1), (-1, 0), (1, 0)}


def get_neighbors(input: Input, coord: Coord) -> List[Coord]:
    x, y = coord
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(input[0]) and 0 <= ny < len(input) and input[ny][nx] != "#":
            neighbors.append((nx, ny))
    return neighbors


# Increase recursion limit
sys.setrecursionlimit(10000)


def find_longest_path(
    input: Input,
    part2: bool = False,
    start: Coord = (1, 0),
    visited: Set[Coord] = set(),
) -> Set[Coord]:
    current = start
    while current[1] != len(input) - 1:
        x, y = current
        visited.add(current)
        value = input[y][x]
        # If current is a slope, move in that direction
        if not part2 and value in "^v<>":
            if value == "^":
                current = (x, y - 1)
            elif value == "v":
                current = (x, y + 1)
            elif value == "<":
                current = (x - 1, y)
            elif value == ">":
                current = (x + 1, y)
            # If current is visited, we done fucked up
            if current in visited:
                return set()
            continue
        neighbors = get_neighbors(input, current)
        # Skip visited neighbors
        neighbors = [neighbor for neighbor in neighbors if neighbor not in visited]
        # If we there are more possible neighbors, take the max of either direction
        if len(neighbors) > 1:
            solutions = (
                find_longest_path(input, part2, neighbor, visited.copy())
                for neighbor in neighbors
            )
            # Return the solution which is the longest
            return max(solutions, key=len)

        if len(neighbors) == 0:
            return set()

        current = neighbors[0]

    return visited


def part1(input: Input) -> None:
    longest_path = find_longest_path(input)
    print("Part 1:", len(longest_path))


def part2(input: Input) -> None:
    longest_path = find_longest_path(input, True)
    print("Part 2:", len(longest_path))


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    # part1(input)
    part2(input)
