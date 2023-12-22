from typing import Dict, List, Set, Tuple


def range_intersection(a: range, b: range) -> bool:
    return bool(range(max(a.start, b.start), min(a.stop, b.stop)))


class Brick:
    def __init__(self, x: range, y: range, z: range) -> None:
        self.x = x
        self.y = y
        self.z = z

    def fall_down(self) -> "Brick":
        return Brick(self.x, self.y, range(self.z.start - 1, self.z.stop - 1))

    def intersects(self, other: "Brick") -> bool:
        return (
            range_intersection(self.x, other.x)
            and range_intersection(self.y, other.y)
            and range_intersection(self.z, other.z)
        )

    def is_directly_above(self, other: "Brick") -> bool:
        return (
            range_intersection(self.x, other.x)
            and range_intersection(self.y, other.y)
            and self.z.start == other.z.stop
        )

    def is_directly_below(self, other: "Brick") -> bool:
        return (
            range_intersection(self.x, other.x)
            and range_intersection(self.y, other.y)
            and self.z.stop == other.z.start
        )

    def __repr__(self) -> str:
        return f"Brick(x={self.x}, y={self.y}, z={self.z})\n"

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))


Bricks = List[Brick]


def parse_input(input: List[str]) -> Bricks:
    bricks: Bricks = []

    for line in input:
        parts = line.strip().split("~")

        x1, y1, z1 = parts[0].split(",")
        x2, y2, z2 = parts[1].split(",")

        bricks.append(
            Brick(
                range(int(x1), int(x2) + 1),
                range(int(y1), int(y2) + 1),
                range(int(z1), int(z2) + 1),
            )
        )

    return bricks


def fall_down(bricks: Bricks) -> Tuple[Bricks, bool]:
    # Make brick fall down if not
    # 1. Its on the ground
    # 2. It intersects with another brick

    new_bricks: Bricks = []
    did_change = False
    for brick in bricks:
        if brick.z.start == 0:
            new_bricks.append(brick)
            continue
        next_brick = brick.fall_down()
        does_intersect = False
        for other in bricks:
            if brick == other:
                continue
            if next_brick.intersects(other):
                does_intersect = True
                break
        if not does_intersect:
            new_bricks.append(next_brick)
            did_change = True
        else:
            new_bricks.append(brick)

    return new_bricks, did_change


SupportMap = Dict[Brick, Set[Brick]]


def get_support_map(bricks: Bricks) -> Tuple[SupportMap, SupportMap]:
    # For each brick, find all bricks that support it
    support_map: SupportMap = {}
    supported_by: SupportMap = {}
    for brick in bricks:
        support_map[brick] = set()
        supported_by[brick] = set()
        for other in bricks:
            if brick == other:
                continue
            if brick.is_directly_above(other):
                supported_by[brick].add(other)
            if brick.is_directly_below(other):
                support_map[brick].add(other)

    return support_map, supported_by


def part1(bricks: Bricks) -> None:
    did_change = True
    while did_change:
        bricks, did_change = fall_down(bricks)

    support_map, supported_by = get_support_map(bricks)

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


def main(lines: List[str]) -> None:
    input = parse_input(lines)
    part1(input)
