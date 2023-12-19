import re
from typing import Dict, List, Literal, Tuple, cast

Operator = Literal[">", "<"]
# (variable, operator, value, target rule) | (target rule)
Rule = Tuple[str, Operator, int, str] | str
# (workflow name -> rules)
Workflows = Dict[str, List[Rule]]
# Collection of variables
Parts = List[Dict[str, int]]

# Workflows are in the format <name>{<variable><operator><value>:<target rule>, ...}
workflow_regex = re.compile(r"(\w+){(.+)}")
rule_regex = re.compile(r"(\w)(<|>)(\d+):(\w+)")


def parse_input(lines: List[str]) -> Tuple[Workflows, Parts]:
    break_index = lines.index("\n")
    workflows: Workflows = {}
    for workflow in lines[:break_index]:
        workflow_match = workflow_regex.match(workflow.strip())
        assert workflow_match is not None
        workflow_name = workflow_match.group(1)
        rules = workflow_match.group(2).split(",")
        # All except last rule
        for rule in rules[:-1]:
            rule_match = rule_regex.match(rule)
            assert rule_match is not None
            assert len(rule_match.groups()) == 4
            variable, operator, value, target_rule = rule_match.groups()
            workflows.setdefault(workflow_name, []).append(
                (variable, cast(Operator, operator), int(value), target_rule)
            )
        # Last rule is always just a target rule
        workflows.setdefault(workflow_name, []).append(rules[-1])

    parts: Parts = []
    for parts_dict_str in lines[break_index + 1 :]:
        parts_dict_str = parts_dict_str.strip().removeprefix("{").removesuffix("}")
        parts_str = parts_dict_str.split(",")
        parts.append(
            {p[0]: int(p[1]) for part_str in parts_str if (p := part_str.split("="))}
        )

    return workflows, parts


def part1(workflows: Workflows, parts: Parts) -> None:
    accepted: Parts = []
    for rating in parts:
        current = "in"
        while current != "A" and current != "R":
            rules = workflows[current]
            for rule in rules:
                if isinstance(rule, str):
                    current = rule
                    break
                variable, operator, value, target_rule = rule
                if operator == ">":
                    if rating[variable] > value:
                        current = target_rule
                        break
                elif operator == "<":
                    if rating[variable] < value:
                        current = target_rule
                        break
        if current == "A":
            accepted.append(rating)

    # Sum all the values of the accepted parts
    result = sum(sum(part.values()) for part in accepted)
    print("Part 1:", result)


def part2(workflows: Workflows) -> None:
    # We need to reverse the workflows to determine the possible values for each
    # variable for it to reach A
    Range = Tuple[int, int]
    # (x, m, a, s)
    Ranges = List[Range]

    def variable_to_index(variable: str) -> int:
        return "xmas".index(variable)

    def adjust_ranges(
        variable: str, operator: Operator, value: int, ranges: List[Ranges]
    ) -> List[Ranges]:
        """
        Adjust the ranges so that the given condition is true
        """
        index = variable_to_index(variable)
        for range in ranges:
            low, high = range[index]
            if operator == ">":
                low = max(low, value + 1)
            elif operator == "<":
                high = min(high, value - 1)
            if low > high:
                continue
            range[index] = (low, high)
        return ranges

    def dfs_inner(rules: List[Rule]) -> List[Ranges]:
        rule = rules[0]
        if isinstance(rule, str):
            # This is a target rule, use the outer function
            return dfs(rule)
        rest = rules[1:]
        variable, operator, value, target_rule = rule

        # This will be the result if the condition is true
        if_true = adjust_ranges(variable, operator, value, dfs(target_rule))

        # This will be the result if the condition is false
        # Inverse the operator and value
        inverse_operator: Operator = ">" if operator == "<" else "<"
        inverse_value = value - 1 if operator == "<" else value + 1
        if_false = adjust_ranges(
            variable, inverse_operator, inverse_value, dfs_inner(rest)
        )

        return if_true + if_false

    def dfs(workflow_name: str) -> List[Ranges]:
        if workflow_name == "R":
            return []
        if workflow_name == "A":
            return [[(1, 4000), (1, 4000), (1, 4000), (1, 4000)]]
        return dfs_inner(workflows[workflow_name])

    result = 0
    for range in dfs("in"):
        value = 1
        # Multiply the ranges together to get the number of possible values
        for low, high in range:
            value *= high - low + 1
        result += value

    print("Part 2:", result)


def main(lines: List[str]) -> None:
    workflows, parts = parse_input(lines)
    part1(workflows, parts)
    part2(workflows)
