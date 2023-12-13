from typing import List, cast

Grid = List[List[str]]
Input = List[Grid]


def parse_input(lines: List[str]) -> Input:
    input: Input = []
    current: Grid = []
    for line in lines:
        if line.strip() == "":
            input.append(current)
            current = []
            continue
        current.append(list(line.strip()))
    input.append(current)
    return input


def print_grid(grid: Grid) -> None:
    print()
    for row in grid:
        print("".join(row))


def part1(input: Input) -> None:
    def test_grid(grid: Grid, i: int) -> int:
        left_index = i - 1
        right_index = i
        while left_index >= 0 and right_index < len(grid):
            left = grid[left_index]
            right = grid[right_index]
            if "".join(left) != "".join(right):
                return False
            left_index -= 1
            right_index += 1

        return True

    def pattern_notes(grid: Grid) -> int:
        transposed_grid = cast(Grid, list(zip(*grid)))
        # First try and find a reflection along the y-axis
        for y in range(1, len(grid)):
            is_valid = test_grid(grid, y)
            if is_valid:
                return y * 100
        # Then try and find a reflection along the y-axis

        for x in range(1, len(transposed_grid)):
            is_valid = test_grid(transposed_grid, x)
            if is_valid:
                return x
        return 0

    result = 0
    for grid in input:
        result += pattern_notes(grid)
    print(f"Part 1: {result}")


def part2(input: Input) -> None:
    def check_for_smudge(left_row: List[str], right_row: List[str]) -> bool:
        differences = 0
        for left, right in zip(left_row, right_row):
            if left != right:
                differences += 1
            if differences > 1:
                return False
        return differences == 1

    def test_grid(grid: Grid, i: int) -> int:
        has_fixed_smudge = False
        left_index = i - 1
        right_index = i
        while left_index >= 0 and right_index < len(grid):
            left = grid[left_index]
            right = grid[right_index]
            if "".join(left) != "".join(right):
                if not has_fixed_smudge and check_for_smudge(left, right):
                    has_fixed_smudge = True
                else:
                    return False
            left_index -= 1
            right_index += 1

        return has_fixed_smudge

    def pattern_notes(grid: Grid) -> int:
        transposed_grid = cast(Grid, list(zip(*grid)))
        # First try and find a reflection along the y-axis
        for y in range(1, len(grid)):
            is_valid = test_grid(grid, y)
            if is_valid:
                return y * 100

        # Then try and find a reflection along the y-axis
        for x in range(1, len(transposed_grid)):
            is_valid = test_grid(transposed_grid, x)
            if is_valid:
                return x
        return 0

    result = 0
    for grid in input:
        result += pattern_notes(grid)
    print(f"Part 2: {result}")


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
