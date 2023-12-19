from typing import Dict, List, Literal, Set, Tuple, cast

Direction = Literal["U", "D", "L", "R"]
# (direction, steps, hex color)
Instruction = Tuple[Direction, int]
Coord = Tuple[int, int]


def parse_input(lines: List[str]) -> Tuple[List[Instruction], List[str]]:
    return [
        (
            cast(Direction, parts[0]),
            int(parts[1]),
        )
        for line in lines
        if (parts := line.strip().split(" "))
    ], [
        parts[2].removeprefix("(#").removesuffix(")")
        for line in lines
        if (parts := line.strip().split(" "))
    ]


def dig(instructions: List[Instruction]) -> Set[Coord]:
    trench: Set[Coord] = set()
    current = (0, 0)
    trench.add(current)
    for instruction in instructions:
        direction, steps = instruction
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


def get_enclosed_intervals(trench: Set[Coord]) -> List[Coord]:
    # Group each trench by the y coordinate
    trench_by_y: Dict[int, List[int]] = {}
    for x, y in trench:
        trench_by_y.setdefault(y, []).append(x)

    # Sort each trench by the x coordinate
    for y in trench_by_y:
        trench_by_y[y] = sorted(trench_by_y[y])

    enclosed_intervals: List[Coord] = []

    for y, xs in trench_by_y.items():
        start: int | None = None

        in_direction: None | Direction = None
        straight_line: bool = True
        parity = 0

        for x in xs:
            # If we turn right, coming in from either up or down,
            # this is the end of an interval
            if (x + 1, y) in trench and (x - 1, y) not in trench:
                if start is not None:
                    enclosed_intervals.append((start, x))
                    start = None

                straight_line = True
                # Set the in direction
                if (x, y + 1) in trench:
                    in_direction = "D"
                elif (x, y - 1) in trench:
                    in_direction = "U"
                else:
                    raise ValueError("Invalid trench")
                continue

            # If a turn up or down, coming in from the left,
            # this is the start of an interval.
            # If and only if we have not moved in a straight line from the left and
            # coming in from the same direction.
            if (x + 1, y) not in trench and (x - 1, y) in trench:
                # Get the direction this turn originates from (up or down)
                if (x, y + 1) in trench:
                    dir = "D"
                elif (x, y - 1) in trench:
                    dir = "U"
                else:
                    raise ValueError("Invalid trench")
                # If we are coming in from the same direction as the previous turn,
                # and we have moved in a straight line from the left, continue
                if straight_line and in_direction != dir:
                    parity += 1
                if parity % 2 == 1:
                    start = x

                straight_line = False
                in_direction = None
                continue
            # If a vertical line, this could be either the start or end of an interval
            if (x, y + 1) in trench and (x, y - 1) in trench:
                if start is None:
                    start = x
                else:
                    enclosed_intervals.append((start, x))
                    start = None
                parity += 1
                in_direction = None
                straight_line = False
            # If a straight horizontal line, continue
            if (x + 1, y) not in trench:
                straight_line = False

    return enclosed_intervals


def count_enclosed_area(trench: Set[Coord]) -> int:
    enclosed_intervals = get_enclosed_intervals(trench)
    return sum(end - start - 1 for start, end in enclosed_intervals)


def part1(instructions: List[Instruction]) -> None:
    trench = dig(instructions)
    area = count_enclosed_area(trench) + len(trench)
    print("Part 1:", area)


def part2(hexes: List[str]) -> None:
    # Hex consists of 6 digits, where the 5 digits are the distance and the last digit
    # is the direction
    # 0 = R, 1 = D, 2 = L, 3 = U
    instructions = [
        (cast(Direction, "RDLU"[int(hex[-1])]), int(hex[:-1], 16)) for hex in hexes
    ]
    trench = dig(instructions)
    area = count_enclosed_area(trench) + len(trench)
    print("Part 2:", area)


def main(lines: List[str]) -> None:
    instructions, hex = parse_input(lines)
    part1(instructions)
    part2(hex)
