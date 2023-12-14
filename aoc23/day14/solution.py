from typing import List, Tuple

Input = List[List[str]]
Coord = Tuple[int, int]


def parse_input(lines: List[str]) -> List[List[str]]:
    return [list(line.strip()) for line in lines]


def print_input(input: Input) -> None:
    print()
    for line in input:
        print("".join(line))


def part1(input: Input) -> None:
    def move_up(coord: Coord, input: Input) -> Input:
        x, y = coord
        input[y][x] = "."
        next_y = y
        while next_y > 0 and input[next_y - 1][x] == ".":
            next_y -= 1
        input[next_y][x] = "O"
        return input

    def tilt_lever(input: Input) -> Input:
        for y, line in enumerate(input):
            for x, c in enumerate(line):
                if c == "O":
                    input = move_up((x, y), input)
        return input

    def get_load(input: Input) -> int:
        load = 0
        for y, line in enumerate(input):
            for c in line:
                if c == "O":
                    load += len(input) - y
        return load

    input = tilt_lever(input)
    load = get_load(input)

    print(f"Part 1: {load}")


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
