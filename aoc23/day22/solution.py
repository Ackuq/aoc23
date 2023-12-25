from typing import Dict, List, Set, Tuple


def range_intersection(a: range, b: range) -> bool:
    return bool(range(max(a.start, b.start), min(a.stop, b.stop)))


Brick = Tuple[range, range, range]


def brick_fall_down(brick: Brick) -> Brick:
    return (brick[0], brick[1], range(brick[2].start - 1, brick[2].stop - 1))


def intersects(brick1: Brick, brick2: Brick) -> bool:
    return (
        range_intersection(brick1[0], brick2[0])
        and range_intersection(brick1[1], brick2[1])
        and range_intersection(brick1[2], brick2[2])
    )


def is_directly_above(brick1: Brick, brick2: Brick) -> bool:
    return (
        range_intersection(brick1[0], brick2[0])
        and range_intersection(brick1[1], brick2[1])
        and brick1[2].start == brick2[2].stop
    )


def is_directly_below(brick1: Brick, brick2: Brick) -> bool:
    return (
        range_intersection(brick1[0], brick2[0])
        and range_intersection(brick1[1], brick2[1])
        and brick1[2].stop == brick2[2].start
    )


def parse_input(input: List[str]) -> List[Brick]:
    bricks: List[Brick] = []

    for line in input:
        parts = line.strip().split("~")

        x1, y1, z1 = parts[0].split(",")
        x2, y2, z2 = parts[1].split(",")

        bricks.append(
            (
                range(int(x1), int(x2) + 1),
                range(int(y1), int(y2) + 1),
                range(int(z1), int(z2) + 1),
            )
        )

    return bricks


def fall_down(bricks: List[Brick]) -> Tuple[List[Brick], bool]:
    # Make brick fall down if not
    # 1. Its on the ground
    # 2. It intersects with another brick

    new_bricks: List[Brick] = []
    did_change = False
    for brick in bricks:
        if brick[2].start == 0:
            new_bricks.append(brick)
            continue
        next_brick = brick_fall_down(brick)
        does_intersect = False
        for other in bricks:
            if brick == other:
                continue
            if intersects(brick, other):
                does_intersect = True
                break
        if not does_intersect:
            new_bricks.append(next_brick)
            did_change = True
        else:
            new_bricks.append(brick)

    return new_bricks, did_change


SupportMap = Dict[Brick, Set[Brick]]


def get_support_map(bricks: List[Brick]) -> Tuple[SupportMap, SupportMap]:
    # For each brick, find all bricks that support it
    support_map: SupportMap = {}
    supported_by: SupportMap = {}
    for brick in bricks:
        support_map[brick] = set()
        supported_by[brick] = set()
        for other in bricks:
            if brick == other:
                continue
            if is_directly_above(brick, other):
                supported_by[brick].add(other)
            if is_directly_below(brick, other):
                support_map[brick].add(other)

    return support_map, supported_by


def part1(
    bricks: List[Brick], support_map: SupportMap, supported_by: SupportMap
) -> None:
    count = 0
    # Find bricks that either does not support any other brick
    # or support bricks that are supported by other bricks
    for brick in bricks:
        if len(support_map[brick]) == 0:
            count += 1
            continue

        all_supported = all(len(supported_by[b]) > 1 for b in support_map[brick])
        if all_supported:
            count += 1

    print("Part 1:", count)


def part2(
    bricks: List[Brick], support_map: SupportMap, supported_by: SupportMap
) -> None:
    count = 0
    for brick in bricks:
        # Keep track of bricks that have fallen / been removed
        fallen = {brick}
        possible_fallers = set(support_map[brick])
        while len(possible_fallers) > 0:
            # Get the next brick that could fall
            next_faller = possible_fallers.pop()
            # If it has already fallen, continue
            if next_faller in fallen:
                continue
            # Check if it is supported by any bricks that have not fallen
            if all(support in fallen for support in supported_by[next_faller]):
                fallen.add(next_faller)
                possible_fallers.update(support_map[next_faller])
        count += len(fallen) - 1
    print("Part 2:", count)


def main(lines: List[str]) -> None:  #
    bricks = parse_input(lines)
    did_change = True
    while did_change:
        bricks, did_change = fall_down(bricks)
    support_map, supported_by = get_support_map(bricks)
    part1(bricks, support_map, supported_by)
    part2(bricks, support_map, supported_by)
