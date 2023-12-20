from copy import deepcopy
from typing import Dict, List, Literal, Tuple, cast

Pulse = Literal["high", "low"]
FlipFlopState = Literal["on", "off"]
Conjunction = Dict[str, Pulse]

Module = (
    Tuple[Literal["broadcaster"], List[str]]
    | Tuple[Literal["flip-flop"], FlipFlopState, List[str]]
    | Tuple[Literal["conjunction"], Conjunction, List[str]]
)

States = Dict[str, Module]


def parse_input(lines: List[str]) -> States:
    states: States = {}
    for line in lines:
        module, targets_str = line.strip().split(" -> ")
        targets = targets_str.split(", ")
        if module == "broadcaster":
            states["broadcaster"] = ("broadcaster", targets)
        elif module.startswith("%"):
            module_name = module[1:]
            states[module_name] = ("flip-flop", "off", targets)
        elif module.startswith("&"):
            module_name = module[1:]
            states[module_name] = ("conjunction", {}, targets)
        else:
            raise ValueError(f"Unknown module {module}")
    # Get all of the modules pointing to conjunction and update the conjunction's memory
    for key, m in states.items():
        target_modules = m[1] if m[0] == "broadcaster" else m[2]
        for target in target_modules:
            if target not in states:
                continue
            if states[target][0] == "conjunction":
                cast(Conjunction, states[target][1])[key] = "low"

    return states


# The signals needs to be sent in a BFS manner.
# I.e. send all signals to all targets, then send all signals to all targets of
# those targets, etc.
def bfs(states: States) -> Tuple[States, int, int]:
    low_pulses = 0
    high_pulses = 0
    # Start by sending low pulse to broadcaster
    queue: List[Tuple[str, str, Pulse]] = [("button", "broadcaster", "low")]
    while queue:
        sender, current, signal = queue.pop(0)
        # print(f"{sender} -{signal}-> {current}")
        if signal == "low":
            low_pulses += 1
        else:
            high_pulses += 1

        if current not in states:
            continue
        current_module = states[current]
        if current_module[0] == "broadcaster":
            targets = current_module[1]
            # Broadcast the signal to all targets
            for target in targets:
                queue.append((current, target, signal))
        elif current_module[0] == "flip-flop":
            if signal == "high":
                # If flip-flop receives high, nothing happens
                continue
            state = current_module[1]
            targets = current_module[2]
            # If flip flop receives low
            # If flip flop is off, turn on and send high
            # If flip flop is on, turn off and send low
            next_state: FlipFlopState = "on" if state == "off" else "off"
            next_signal: Pulse = "high" if state == "off" else "low"
            states[current] = (
                "flip-flop",
                next_state,
                current_module[2],
            )
            for target in targets:
                queue.append((current, target, next_signal))

        elif current_module[0] == "conjunction":
            # First update the memory
            cast(Conjunction, current_module[1])[sender] = signal
            # Send low pulse to all targets if all signals are high
            # Otherwise send high
            next_signal = (
                "low"
                if all(
                    input == "high"
                    for input in cast(Conjunction, current_module[1]).values()
                )
                else "high"
            )
            targets = current_module[2]
            for target in targets:
                queue.append((current, target, next_signal))

    return states, low_pulses, high_pulses


def part1(states: States) -> None:
    states = deepcopy(states)
    low_pulses = 0
    high_pulses = 0
    for _ in range(1000):
        states, low, high = bfs(states)
        low_pulses += low
        high_pulses += high

    # print("Low pulses", low_pulses)
    # print("High pulses", high_pulses)
    print(
        "Part 1",
        low_pulses * high_pulses,
    )


def bfs2(
    states: States, presses: int, modules_to_check: Dict[str, int | None]
) -> Tuple[States, Dict[str, int | None]]:
    # Start by sending low pulse to broadcaster
    queue: List[Tuple[str, str, Pulse]] = [("button", "broadcaster", "low")]
    while queue:
        sender, current, signal = queue.pop(0)
        # print(f"{sender} -{signal}-> {current}")

        if current not in states:
            continue
        current_module = states[current]
        if current_module[0] == "broadcaster":
            targets = current_module[1]
            # Broadcast the signal to all targets
            for target in targets:
                queue.append((current, target, signal))
        elif current_module[0] == "flip-flop":
            if signal == "high":
                # If flip-flop receives high, nothing happens
                continue
            state = current_module[1]
            targets = current_module[2]
            # If flip flop receives low
            # If flip flop is off, turn on and send high
            # If flip flop is on, turn off and send low
            next_state: FlipFlopState = "on" if state == "off" else "off"
            next_signal: Pulse = "high" if state == "off" else "low"
            states[current] = (
                "flip-flop",
                next_state,
                current_module[2],
            )
            for target in targets:
                queue.append((current, target, next_signal))

        elif current_module[0] == "conjunction":
            # First update the memory
            cast(Conjunction, current_module[1])[sender] = signal
            # Send low pulse to all targets if all signals are high
            # Otherwise send high
            next_signal = (
                "low"
                if all(
                    input == "high"
                    for input in cast(Conjunction, current_module[1]).values()
                )
                else "high"
            )
            if (
                next_signal == "high"
                and current in modules_to_check
                and modules_to_check[current] is None
            ):
                modules_to_check[current] = presses
            targets = current_module[2]
            for target in targets:
                queue.append((current, target, next_signal))

    return states, modules_to_check


def part2(states: States) -> None:
    states = deepcopy(states)

    # rx is only pointed from one module, which is a conjunction of conjunctions
    # create a map of when all of the conjunctions are high
    module_to_rx: str | None = None
    for key, state in states.items():
        if state[0] == "conjunction" and "rx" in state[2]:
            module_to_rx = key
            break
    assert module_to_rx is not None
    modules_to_check: Dict[str, int | None] = {}
    for key, state in states.items():
        if state[0] == "conjunction" and module_to_rx in state[2]:
            modules_to_check[key] = None

    button_presses = 0
    while True:
        button_presses += 1
        states, modules_to_check = bfs2(states, button_presses, modules_to_check)
        if all(v is not None for v in modules_to_check.values()):
            break

    # Get all of the values from the modules
    values = [v for v in modules_to_check.values() if v is not None]

    # Get the lowest common multiple of all of the values
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    lcm = values[0]
    for i in values[1:]:
        lcm = lcm * i // gcd(lcm, i)

    # print("Low pulses", low_pulses)
    # print("High pulses", high_pulses)
    print("Part 2", lcm)


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
    part2(input)
