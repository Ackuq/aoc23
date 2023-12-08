import re
from typing import Dict, List, Literal, Tuple

Instruction = Literal["L"] | Literal["R"]

Mapping = Dict[str, Tuple[str, str]]

Input = Tuple[List[str], Mapping]

regex = r"(.+) = \((.+), (.+)\)"


def parse_input(lines: List[str]) -> Input:
    instructions = list(lines[0].strip())
    mapping: Mapping = {}

    for line in lines[2:]:
        match = re.match(regex, line.strip())
        assert match is not None
        mapping[match.group(1)] = (match.group(2), match.group(3))

    return (instructions, mapping)


def part1(input: Input) -> None:
    instructions, mapping = input
    current = "AAA"
    if current not in mapping:
        return None
    instruction_index = 0
    steps = 0
    while current != "ZZZ":
        instruction = instructions[instruction_index]
        current = mapping[current][0] if instruction == "L" else mapping[current][1]
        instruction_index += 1
        steps += 1
        if instruction_index == len(instructions):
            instruction_index = 0

    print("Part 1:", steps)


def part2(input: Input) -> None:
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def lcm(a: int, b: int) -> int:
        return a * b // gcd(a, b)

    instructions, mapping = input
    nodes = set(node for node in mapping.keys() if node.endswith("A"))
    instruction_index = 0
    steps = 0
    multiply = 1
    while len(nodes) > 0:
        instruction = instructions[instruction_index]
        if any(node.endswith("Z") for node in nodes):
            multiply = lcm(multiply, steps)
        nodes = set(
            mapping[node][0] if instruction == "L" else mapping[node][1]
            for node in nodes
            if not node.endswith("Z")
        )
        instruction_index += 1
        steps += 1
        if instruction_index == len(instructions):
            instruction_index = 0

    print("Part 2:", multiply)


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
