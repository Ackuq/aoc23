from typing import Dict, List, Literal, Tuple, cast

Direction = Literal["U", "D", "L", "R"]
# (direction, steps, hex color)
Instruction = Tuple[Direction, int]
Coord = Tuple[int, int]

direction_to_coord: Dict[Direction, Coord] = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


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


def get_area(instructions: List[Instruction]) -> int:
    position = 0
    area = 1.0

    for direction, steps in instructions:
        dx, dy = direction_to_coord[direction]
        position += dx * steps
        area += dy * steps * position + steps / 2

    return int(area)


def part1(instructions: List[Instruction]) -> None:
    area = get_area(instructions)
    print("Part 1:", area)


def part2(hexes: List[str]) -> None:
    # Hex consists of 6 digits, where the 5 digits are the distance and the last digit
    # is the direction
    # 0 = R, 1 = D, 2 = L, 3 = U
    instructions = [
        (cast(Direction, "RDLU"[int(hex[-1])]), int(hex[:-1], 16)) for hex in hexes
    ]
    area = get_area(instructions)
    print("Part 2:", area)


def main(lines: List[str]) -> None:
    instructions, hex = parse_input(lines)
    part1(instructions)
    part2(hex)
