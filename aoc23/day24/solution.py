from typing import List, Tuple

Coord = Tuple[int, int, int]
Velocity = Coord
# (starting position, velocity)
Hailstone = Tuple[Coord, Velocity]
Input = List[Hailstone]


def parse_line(lines: List[str]) -> Input:
    hailstones: Input = []
    for line in lines:
        starting, velocity = line.strip().split(" @ ")
        x, y, z = starting.split(", ")
        dx, dy, dz = velocity.split(", ")
        hailstones.append(((int(x), int(y), int(z)), (int(dx), int(dy), int(dz))))
    return hailstones


def part1(hailstones: Input) -> None:
    # min = 7
    # max = 27
    min = 200_000_000_000_000
    max = 400_000_000_000_000

    def intersect(h1: Hailstone, h2: Hailstone) -> bool:
        # Check that where these two lines intersect is within the test area
        # Disregard the z axis
        (x1, y1, _), (dx1, dy1, _) = h1
        (x2, y2, _), (dx2, dy2, _) = h2

        # Check if the lines are parallel
        if dx1 * dy2 == dx2 * dy1:
            return False
        # Solve for t
        t = (dx1 * (y2 - y1) + dy1 * (x1 - x2)) / (dx2 * dy1 - dx1 * dy2)
        # Get the intersection point
        x = x2 + t * dx2
        y = y2 + t * dy2

        # Check if intersection is in the past
        if (
            (x < x1 and dx1 > 0)
            or (x > x1 and dx1 < 0)
            or (y < y1 and dy1 > 0)
            or (y > y1 and dy1 < 0)
            or (x < x2 and dx2 > 0)
            or (x > x2 and dx2 < 0)
            or (y < y2 and dy2 > 0)
            or (y > y2 and dy2 < 0)
        ):
            return False

        # Check if the intersection is within the test area
        if min <= x <= max and min <= y <= max:
            return True

        return False

    # Check how many hailstones intersect within the test area
    count = 0
    for i, hailstone in enumerate(hailstones):
        for other in hailstones[(i + 1) :]:
            if intersect(hailstone, other):
                count += 1

    print("Part 1:", count)


def main(lines: List[str]) -> None:
    input = parse_line(lines)
    part1(input)
