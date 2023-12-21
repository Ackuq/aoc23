from typing import Dict, List, Literal, Tuple, cast

Coord = Tuple[int, int]
Cell = Literal[".", "#"]
Grid = List[List[Cell]]


def parse_input(input: List[str]) -> Tuple[Grid, Coord]:
    grid: Grid = []
    start: Coord | None = None
    for y, line in enumerate(input):
        row: List[Cell] = []
        for x, c in enumerate(line.strip()):
            if c == "S":
                start = (x, y)
                row.append(".")
                continue
            row.append(cast(Cell, c))
        grid.append(row)

    assert start is not None
    return grid, start


Distances = Dict[Coord, int]


# Do BFS to get the distance to each cell in x steps
def bfs(grid: Grid, steps: int, start: Coord) -> Distances:
    queue: List[Tuple[Coord, int]] = [(start, 0)]
    distances: Distances = {}
    while queue:
        coord, dist = queue.pop(0)
        if coord in distances:
            continue
        distances[coord] = dist
        x, y = coord
        if dist == steps:
            continue
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_coord = (x + dx, y + dy)
            # Make sure that we don't go out of bounds
            if (
                new_coord[0] < 0
                or new_coord[1] < 0
                or new_coord[0] >= len(grid[0])
                or new_coord[1] >= len(grid)
            ):
                continue
            # Make sure that we don't go through walls
            if grid[new_coord[1]][new_coord[0]] == "#":
                continue

            queue.append((new_coord, dist + 1))
    return distances


def part1(grid: Grid, start: Coord) -> None:
    steps = 64
    parity = steps % 2
    distances = bfs(grid, steps, start)
    # Get all that have the same parity
    reachable = set(coord for coord, dist in distances.items() if dist % 2 == parity)

    print("Part 1:", len(reachable))


def part2(grid: Grid, start: Coord) -> None:
    # Number of steps
    steps = 26501365
    # The length of our input data
    length = len(grid)
    # Get all the distances
    distances = bfs(grid, length, start)

    # Get the corners, they are the ones that take more than the length / 2 to reach
    even_corners = set(
        coord
        for coord, dist in distances.items()
        if dist % 2 == 0 and dist > length // 2
    )
    odd_corners = set(
        coord
        for coord, dist in distances.items()
        if dist % 2 == 1 and dist > length // 2
    )

    # Get all the even and odd cells
    even = set(coord for coord, dist in distances.items() if dist % 2 == 0)
    odd = set(coord for coord, dist in distances.items() if dist % 2 == 1)

    # ((steps - (length / 2)) / length) is the number of grids we reach in
    # one direction
    n = (steps - (length // 2)) // length

    # If we interpret the grid as a diamond,
    result = (
        # The number of odd cells in all directions (including the center, and corners)
        ((n + 1) ** 2) * len(odd)
        # The number of even cells in all directions (excluding the center and corners)
        + (n**2) * len(even)
        # Remove the odd corners,
        - (n + 1) * len(odd_corners)
        # Add the even corners
        + n * len(even_corners)
    )

    print("Part 2:", result)


def main(lines: List[str]) -> None:
    grid, start = parse_input(lines)
    part1(grid, start)
    part2(grid, start)
