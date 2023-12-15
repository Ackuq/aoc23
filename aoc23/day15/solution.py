import re
from typing import Dict, List, Literal, Tuple, cast

Input = List[str]


def parse_input(lines: List[str]) -> Input:
    input = [sequence for sequence in lines[0].strip().split(",")]
    return input


def hash(sequence: str) -> int:
    current_value = 0
    for char in sequence:
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
        # print(current_value)
    return current_value


def part1(input: Input) -> None:
    result = sum(hash(sequence) for sequence in input)
    print(f"Part 1: {result}")


def part2(input: Input) -> None:
    Operation = Tuple[str, Literal["+", "-", "="], int]

    operations: List[Operation] = [
        cast(
            Operation,
            (
                match.group(1),
                match.group(2),
                int(match.group(3)) if match.group(3) else 0,
            ),
        )
        for sequence in input
        if (match := re.match("([a-z]+)([+-=])([0-9]+)?", sequence))
    ]

    HashMap = Dict[int, List[Tuple[str, int]]]

    hash_map: HashMap = {hash: [] for hash in range(0, 256)}

    for operation in operations:
        (label, operator, focal_length) = operation
        label_hash = hash(label)
        if operator == "-":
            # Remove any matching labels
            hash_map[label_hash] = [
                (l, length) for (l, length) in hash_map[label_hash] if l != label
            ]
            continue
        if operator == "=" and any(l == label for (l, _) in hash_map[label_hash]):
            # Replace
            hash_map[label_hash] = [
                (label, focal_length) if l == label else (l, length)
                for (l, length) in hash_map[label_hash]
            ]
            continue
        # Add
        hash_map[label_hash].append((label, focal_length))

    def focus_power(hash_map: HashMap) -> int:
        return sum(
            (box + 1) * (slot + 1) * length
            for (box, lenses) in hash_map.items()
            for slot, (_, length) in enumerate(lenses)
        )

    result = focus_power(hash_map)
    print(f"Part 2: {result}")


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
