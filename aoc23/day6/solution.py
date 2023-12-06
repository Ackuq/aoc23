from typing import List, Tuple

Race = Tuple[
    int,
    int,
]
Input = List[Race]


def parse_input(lines: List[str]) -> Input:
    times = [int(number) for number in lines[0].removeprefix("Time:").split()]
    distance = [int(number) for number in lines[1].removeprefix("Distance:").split()]
    return [(time, distance) for time, distance in zip(times, distance)]


def parse_input2(lines: List[str]) -> Race:
    time = int("".join(number for number in lines[0].removeprefix("Time:").split()))
    distance = int(
        "".join(number for number in lines[1].removeprefix("Distance:").split())
    )

    return (time, distance)


def run_race(time: int, distance: int) -> int:
    winning_times = 0
    for i in range(1, time):
        remaining_time = time - i
        distance_traveled = i * remaining_time
        if distance_traveled > distance:
            winning_times += 1

    return winning_times


def part1(input: Input) -> None:
    result = 1
    for time, distance in input:
        result *= run_race(time, distance)

    print("Part 1:", result)


def part2(input: Race) -> None:
    (time, distance) = input
    result = run_race(time, distance)
    print("Part 2:", result)


def main(lines: List[str]) -> None:
    part1(parse_input(lines))
    part2(parse_input2(lines))
