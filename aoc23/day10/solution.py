import re
from typing import Dict, List, Tuple

Coord = Tuple[int, int]


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.


def get_next_positions(position: Coord, lines: List[str]) -> List[Coord]:
    x, y = position
    character = lines[y][x]

    if character == "|":
        return [(x, y - 1), (x, y + 1)]
    elif character == "-":
        return [(x - 1, y), (x + 1, y)]
    elif character == "L":
        return [(x + 1, y), (x, y - 1)]
    elif character == "J":
        return [(x - 1, y), (x, y - 1)]
    elif character == "7":
        return [(x - 1, y), (x, y + 1)]
    elif character == "F":
        return [(x + 1, y), (x, y + 1)]
    elif character == "S":
        return predict_next_positions(position, lines)

    return []


def predict_next_positions(position: Coord, lines: List[str]) -> List[Coord]:
    x, y = position
    next_positions: List[Coord] = []

    # Up
    if y > 0 and lines[y - 1][x] in "|7F":
        next_positions.append((x, y - 1))
    # Down
    if y < len(lines) - 1 and lines[y + 1][x] in "|LJ":
        next_positions.append((x, y + 1))
    # Left
    if x > 0 and lines[y][x - 1] in "-LF":
        next_positions.append((x - 1, y))
    # Right
    if x < len(lines[y]) - 1 and lines[y][x + 1] in "-J7":
        next_positions.append((x + 1, y))
    return next_positions


def get_starting_position(lines: List[str]) -> Coord:
    for y, line in enumerate(lines):
        try:
            return (line.index("S"), y)
        except Exception:
            pass
    raise Exception("No starting position found")


def get_distances(lines: List[str]) -> Dict[Coord, int]:
    # Coordinate -> (number of steps to get there)
    distances: Dict[Coord, int] = {}

    starting_position = get_starting_position(lines)
    next_positions: List[Tuple[Coord, int]] = [(starting_position, 0)]

    while next_positions:
        position, steps = next_positions.pop(0)

        if position in distances:
            continue

        distances[position] = steps

        next_positions.extend(
            (next_position, steps + 1)
            for next_position in get_next_positions(position, lines)
        )

    return distances


def part1(lines: List[str]) -> None:
    distances = get_distances(lines)
    print("Part 1:", max(distances.values()))


def part2(lines: List[str]) -> None:
    distances = get_distances(lines)
    # Replace all of the characters not in the main loop with .
    for y, line in enumerate(lines):
        for x, _ in enumerate(line):
            if (x, y) not in distances:
                lines[y] = lines[y][:x] + "." + lines[y][x + 1 :]

    # We can find the number of enclosed spaces by counting the number of vertical pipes
    enclosed_count = 0
    for line in lines:
        # This might need to be changed depending on the input
        line = re.sub(r"S", "|", line)
        # Collapse all of the 90 degree bends into a single, vertical, character
        line = re.sub(r"L-*7|F-*J", "|", line)

        vertical_count = 0
        for char in line:
            if char == "|":
                vertical_count += 1
            if char == "." and vertical_count % 2 == 1:
                enclosed_count += 1

    print("Part 2:", enclosed_count)


def main(lines: List[str]) -> None:
    part1(lines)
    part2(lines)
