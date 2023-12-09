from typing import List

Input = List[List[int]]


def parse_input(input: List[str]) -> Input:
    return [[int(number) for number in line.strip().split()] for line in input]


def all_zeroes(row: List[int]) -> bool:
    return all([number == 0 for number in row])


def extrapolate(differences: Input, reversed: bool = False) -> int:
    results: List[int] = []
    for difference in differences[::-1]:
        if len(results) == 0:
            results.append(difference[-1])
            continue
        results.append(
            results[-1] + difference[-1]
            if not reversed
            else difference[-1] - results[-1]
        )

    return results[-1]


def get_difference_list(row: List[int], reversed: bool = False) -> Input:
    result: Input = [row]
    current = row
    while not all_zeroes(current):
        next = [
            second - first if not reversed else first - second
            for first, second in zip(current, current[1:])
        ]
        current = next
        result.append(current)
    return result


def part1(input: Input) -> None:
    result = 0
    for row in input:
        differences = get_difference_list(row)
        result += extrapolate(differences)

    print("Part 1:", result)


def part2(input: Input) -> None:
    result = 0
    for row in input:
        differences = get_difference_list(list(reversed(row)), True)
        result += extrapolate(differences, True)

    print("Part 2:", result)


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
