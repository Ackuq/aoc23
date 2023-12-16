from typing import Dict, List, Literal, Set, Tuple, cast

Coord = Tuple[int, int]
Grid = List[List[str]]
Direction = Literal["up", "down", "left", "right"]
State = Tuple[Coord, Direction]


def parse_input(input: List[str]) -> Grid:
    return [list(line.strip()) for line in input]


def get_next_coord(current: Coord, grid: Grid, direction: Direction) -> Coord | None:
    (x, y) = current
    if direction == "up" and y > 0:
        return (x, y - 1)
    elif direction == "down" and y < len(grid) - 1:
        return (x, y + 1)
    elif direction == "left" and x > 0:
        return (x - 1, y)
    elif direction == "right" and x < len(grid[0]) - 1:
        return (x + 1, y)
    return None


def print_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))


def get_next_states(grid: Grid, coord: Coord, direction: Direction) -> List[State]:
    (x, y) = coord
    current = grid[y][x]
    next_states: List[Tuple[Coord | None, Direction]] = []
    if (
        current == "."
        or (current == "|" and (direction == "up" or direction == "down"))
        or (current == "-" and (direction == "left" or direction == "right"))
    ):
        # Continue the beam
        next_states.append((get_next_coord(coord, grid, direction), direction))
    elif current == "|" and (direction == "left" or direction == "right"):
        # Split the beam up and down
        next_states.append((get_next_coord(coord, grid, "up"), "up"))
        next_states.append((get_next_coord(coord, grid, "down"), "down"))
    elif current == "-" and (direction == "up" or direction == "down"):
        # Split the beam left and right
        next_states.append((get_next_coord(coord, grid, "left"), "left"))
        next_states.append((get_next_coord(coord, grid, "right"), "right"))
    elif (current == "/" and direction == "up") or (
        current == "\\" and direction == "down"
    ):
        # Split the beam right
        next_states.append((get_next_coord(coord, grid, "right"), "right"))
    elif (current == "/" and direction == "down") or (
        current == "\\" and direction == "up"
    ):
        # Split the beam left
        next_states.append((get_next_coord(coord, grid, "left"), "left"))
    elif (current == "/" and direction == "left") or (
        current == "\\" and direction == "right"
    ):
        # Split the beam down
        next_states.append((get_next_coord(coord, grid, "down"), "down"))
    elif (current == "/" and direction == "right") or (
        current == "\\" and direction == "left"
    ):
        # Split the beam up
        next_states.append((get_next_coord(coord, grid, "up"), "up"))
    else:
        raise Exception(f"Unknown state: {current} at {coord}")

    # Get next states without next coordinate
    return [
        cast(State, (next_coord, next_direction))
        for (next_coord, next_direction) in next_states
        if next_coord is not None
    ]


def get_energized_tiles(grid: Grid, starting_state: State) -> int:
    visited: Dict[Coord, Set[Direction]] = {}
    next_states: List[State] = [starting_state]

    while len(next_states) > 0:
        next_state = next_states.pop()
        next_coord, next_direction = next_state
        visited.setdefault(next_coord, set())
        if next_direction in visited[next_coord]:
            continue
        visited[next_coord].add(next_direction)
        next_states += get_next_states(grid, next_coord, next_direction)

    return len(visited)


def part1(grid: Grid) -> None:
    result = get_energized_tiles(grid, ((0, 0), "right"))
    print("Part 1:", result)


def part2(grid: Grid) -> None:
    starting_points: List[Tuple[Coord, Direction]] = []
    # Special cases: Edge, can go either direction from the edge
    # Top left corner
    starting_points.append(((0, 0), "right"))
    starting_points.append(((0, 0), "down"))
    # Top right corner
    starting_points.append(((len(grid[0]) - 1, 0), "left"))
    starting_points.append(((len(grid[0]) - 1, 0), "down"))
    # Bottom left corner
    starting_points.append(((0, len(grid) - 1), "up"))
    starting_points.append(((0, len(grid) - 1), "right"))
    # Bottom right corner
    starting_points.append(((len(grid[0]) - 1, len(grid) - 1), "up"))
    starting_points.append(((len(grid[0]) - 1, len(grid) - 1), "left"))
    # Add all along the top and bottom, exclude the corners
    for x in range(1, len(grid[0]) - 1):
        starting_points.append(((x, 0), "down"))
        starting_points.append(((x, len(grid) - 1), "up"))
    # Add all along the left and right, exclude the corners
    for y in range(1, len(grid) - 1):
        starting_points.append(((0, y), "right"))
        starting_points.append(((len(grid[0]) - 1, y), "left"))
    maximum = 0
    for state in starting_points:
        maximum = max(maximum, get_energized_tiles(grid, state))
    print("Part 2:", maximum)


def main(lines: List[str]) -> None:
    grid = parse_input(lines)
    part1(grid)
    part2(grid)
