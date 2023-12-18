import re
from typing import List, Literal, Set, Tuple, cast

Direction = Literal["U", "D", "L", "R"]
# (direction, steps, hex color)
Instruction = Tuple[Direction, int, str]
Coord = Tuple[int, int]


def parse_input(lines: List[str]) -> List[Instruction]:
    return [
        (
            cast(Direction, parts[0]),
            int(parts[1]),
            parts[2].removeprefix("(").removesuffix(")"),
        )
        for line in lines
        if (parts := line.strip().split(" "))
    ]


def print_trench(trench: Set[Coord]) -> None:
    min_x = min(trench, key=lambda c: c[0])[0]
    max_x = max(trench, key=lambda c: c[0])[0]
    min_y = min(trench, key=lambda c: c[1])[1]
    max_y = max(trench, key=lambda c: c[1])[1]

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in trench:
                print("#", end="")
            else:
                print(".", end="")
        print()


def dig(instructions: List[Instruction]) -> Set[Coord]:
    trench: Set[Coord] = set()
    current = (0, 0)
    trench.add(current)
    for instruction in instructions:
        direction, steps, _ = instruction
        for _ in range(steps):
            if direction == "U":
                current = (current[0], current[1] - 1)
            elif direction == "D":
                current = (current[0], current[1] + 1)
            elif direction == "L":
                current = (current[0] - 1, current[1])
            elif direction == "R":
                current = (current[0] + 1, current[1])
            trench.add(current)

    return trench


def get_grid(trench: Set[Coord]) -> List[List[str]]:
    min_x = min(trench, key=lambda c: c[0])[0]
    max_x = max(trench, key=lambda c: c[0])[0]
    min_y = min(trench, key=lambda c: c[1])[1]
    max_y = max(trench, key=lambda c: c[1])[1]

    grid = [["." for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
    for x, y in trench:
        x_index = x - min_x
        y_index = y - min_y
        # If this is an intersection, mark it either F, J, L, 7, -, or |
        if (x + 1, y) in trench and (
            x,
            y + 1,
        ) in trench:
            grid[y_index][x_index] = "F"
        elif (x - 1, y) in trench and (
            x,
            y - 1,
        ) in trench:
            grid[y_index][x_index] = "J"
        elif (x + 1, y) in trench and (x, y - 1) in trench:
            grid[y_index][x_index] = "L"
        elif (x, y + 1) in trench and (
            x - 1,
            y,
        ) in trench:
            grid[y_index][x_index] = "7"
        elif (x + 1, y) in trench and (
            x - 1,
            y,
        ) in trench:
            grid[y_index][x_index] = "-"
        elif (x, y + 1) in trench and (
            x,
            y - 1,
        ) in trench:
            grid[y_index][x_index] = "|"
        else:
            grid[y_index][x_index] = "#"

    return grid


def print_grid(grid: List[List[str]]) -> None:
    for line in grid:
        print("".join(line))


def count_area(grid: List[List[str]]) -> int:
    count = 0
    # First count the perimeter
    for line in grid:
        for char in line:
            # Check if the current character is a vertical connection
            if char != ".":
                count += 1
    # Now count all of the enclosed spaces
    for line in grid:
        # Collapse all of the 90 degree bends into a single, vertical, character
        line_str = re.sub(r"L-*7|F-*J", "|", "".join(line))
        vertical_count = 0
        for char in line_str:
            if char == "|":
                vertical_count += 1
            if char == "." and vertical_count % 2 == 1:
                count += 1
    return count


def part1(instructions: List[Instruction]) -> None:
    trench = dig(instructions)
    grid = get_grid(trench)
    area = count_area(grid)
    print("Part 1:", area)


def main(lines: List[str]) -> None:
    instructions = parse_input(lines)
    part1(instructions)
