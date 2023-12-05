import re
import sys
from typing import Dict, List, Set, Tuple, Union

map_regex = r"(.*)-to-(.*) map"


Maps = List[Tuple[range, int, int, int]]
MapDict = Dict[str, Tuple[str, Maps]]
Input = Tuple[List[int], MapDict]
SeedRange = Tuple[int, int]


def parse_input(input: List[str]) -> Input:
    first_row = input.pop(0)
    seeds = [int(seed) for seed in first_row.removeprefix("seeds: ").split()]
    maps: MapDict = {}
    current_from = ""
    for row in input:
        if row.strip() == "":
            continue
        map_match = re.match(map_regex, row)
        if map_match is not None:
            map_from = map_match.group(1)
            map_to = map_match.group(2)
            current_from = map_from
            maps[map_from] = (map_to, [])
            continue

        [destination, source, step] = [int(i) for i in row.split()]
        maps[current_from][1].append(
            (
                range(source, source + step),
                destination,
                source,
                step,
            )
        )

    return seeds, maps


def by_seed_value(seed: int, maps: MapDict) -> int:
    def get_next_value(current: int, maps: Maps) -> int:
        for r, destination, source, _ in maps:
            if current in r:
                return destination + (current - source)

        return current

    current_type = "seed"
    value = seed
    while current_type != "location":
        (next_type, map) = maps[current_type]
        value = get_next_value(value, map)
        current_type = next_type

    return value


def by_seed_range(seed_ranges: Set[SeedRange], map_dict: MapDict) -> int:
    def get_next_range_or_distance_to_next_range(
        current: int, maps: Maps
    ) -> Union[SeedRange, int]:
        distance_without_match = sys.maxsize
        for r, destination, source, length in maps:
            if current in r:
                offset = current - source
                # Only copy the remaining length, or the length of the range
                # So we don't copy more than we need
                remaining_length = min(length - offset, end - current)
                return (destination + offset, remaining_length)
            elif current < source and (source - current) < distance_without_match:
                # Update our fallback distance, if no match is found
                distance_without_match = source - current
        return distance_without_match

    current_ranges = seed_ranges
    current_type = "seed"
    new_ranges: Set[SeedRange] = set()

    while current_type != "location":
        (next_type, maps) = map_dict[current_type]
        for start, range_length in current_ranges:
            current = start
            end = start + range_length
            while current < end:
                next_range_or_distance = get_next_range_or_distance_to_next_range(
                    current, maps
                )
                if isinstance(next_range_or_distance, int):
                    distance = min(next_range_or_distance, end - current)
                    new_ranges.add((current, distance))
                    current += next_range_or_distance
                    continue
                new_ranges.add(next_range_or_distance)
                current += next_range_or_distance[1]

        current_ranges = new_ranges
        current_type = next_type
        new_ranges = set()

    return min(start for start, _ in current_ranges)


def part1(input: Input) -> None:
    seeds, maps = input

    minimum: int = sys.maxsize

    for seed in seeds:
        value = by_seed_value(seed, maps)
        if value < minimum:
            minimum = value

    print(f"Part 1: {minimum}")


def part2(input: Input) -> None:
    seeds, map_dict = input

    seed_ranges: Set[SeedRange] = set(
        (seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)
    )

    print(f"Part 2: {by_seed_range(seed_ranges, map_dict)}")


def main(input: List[str]) -> None:
    parsed_input = parse_input(input)
    part1(parsed_input)
    part2(parsed_input)
