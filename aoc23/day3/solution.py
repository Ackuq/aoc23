from typing import Dict, List, Set, Tuple

surrounding = [
    [dx, dy] for dx in range(-1, 2) for dy in range(-1, 2) if not (dx == 0 and dy == 0)
]


def part1(input: List[str]) -> None:
    def is_part_number(x1: int, y1: int) -> bool:
        for dx, dy in surrounding:
            x = x1 + dx
            y = y1 + dy
            if x < 0 or y < 0 or y >= len(input) or x >= len(input[y]):
                continue

            if not input[y][x].isdigit() and input[y][x] != "." and input[y][x] != "\n":
                return True

        return False

    result: List[int] = []
    for row_i, row in enumerate(input):
        current_number = ""
        part_number_found = False
        for char_i, char in enumerate(row):
            if not char.isdigit():
                if part_number_found and current_number != "":
                    result.append(int(current_number))
                current_number = ""
                part_number_found = False
                continue

            current_number += char
            if not part_number_found and is_part_number(char_i, row_i):
                part_number_found = True

    print(f"Part 1: {sum(result)}")


def part2(input: List[str]) -> None:
    Coord = Tuple[int, int]
    star_map: Dict[Coord, List[int]] = {}

    def find_stars(x1: int, y1: int) -> List[Coord]:
        stars: List[Coord] = []
        for dx, dy in surrounding:
            x = x1 + dx
            y = y1 + dy
            if x < 0 or y < 0 or y >= len(input) or x >= len(input[y]):
                continue

            if input[y][x] == "*":
                stars.append((x, y))

        return stars

    for row_i, row in enumerate(input):
        current_number = ""
        stars: Set[Coord] = set()
        for char_i, char in enumerate(row):
            if not char.isdigit():
                if current_number != "":
                    for star in stars:
                        if star not in star_map:
                            star_map[star] = []
                        star_map[star].append(int(current_number))
                current_number = ""
                stars = set()
                continue

            current_number += char
            stars.update(find_stars(char_i, row_i))
    result = 0
    for numbers in star_map.values():
        if len(numbers) != 2:
            continue
        result += numbers[0] * numbers[1]

    print(f"Part 2: {result}")


def main(input: List[str]) -> None:
    part1(input)
    part2(input)
