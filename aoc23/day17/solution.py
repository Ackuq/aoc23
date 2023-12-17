from queue import PriorityQueue
from typing import List, Literal, Set, Tuple

City = List[List[int]]
Direction = Literal["up", "down", "left", "right"]
Coord = Tuple[int, int]
# Tuple of (coord, direction, number of steps in same direction, max 3)
Node = Tuple[Coord, Direction | None, int]


def parse_input(lines: List[str]) -> City:
    return [[int(x) for x in line.strip()] for line in lines]


def get_neighbors(city: City, node: Node, min: int, max: int) -> List[Node]:
    (x, y), direction, steps = node
    neighbors: List[Node] = []
    # We can only turn and move in the same direction the maximum times
    if steps < max:
        # Try to move in the same direction
        if direction == "up" and y - 1 >= 0:
            neighbors.append(((x, y - 1), direction, steps + 1))
        elif direction == "down" and y + 1 < len(city):
            neighbors.append(((x, y + 1), direction, steps + 1))
        elif direction == "left" and x - 1 >= 0:
            neighbors.append(((x - 1, y), direction, steps + 1))
        elif direction == "right" and x + 1 < len(city[0]):
            neighbors.append(((x + 1, y), direction, steps + 1))

    # We can turn if we haven't stepped forward the minimum amount times
    # Edge case: if we are at the start, we can turn
    if steps < min and direction is not None:
        return neighbors

    if (direction != "up" and direction != "down") and y - 1 >= 0:
        # Left and right can go up
        neighbors.append(((x, y - 1), "up", 1))
    if (direction != "up" and direction != "down") and y + 1 < len(city):
        # Left and right can go down
        neighbors.append(((x, y + 1), "down", 1))
    if (direction != "left" and direction != "right") and x - 1 >= 0:
        # Up and down can go left
        neighbors.append(((x - 1, y), "left", 1))
    if (direction != "left" and direction != "right") and x + 1 < len(city[0]):
        # Up and down can go right
        neighbors.append(((x + 1, y), "right", 1))

    return neighbors


def dijkstra(city: City, start: Coord, end: Coord, min: int = 0, max: int = 3) -> int:
    queue: PriorityQueue[Tuple[int, Node]] = PriorityQueue()
    visited: Set[Node] = set()
    queue.put((0, (start, None, 0)))
    while not queue.empty():
        acc, node = queue.get()
        if node in visited:
            continue
        if node[0] == end and node[2] >= min:
            return acc
        visited.add(node)
        for neighbor in get_neighbors(city, node, min, max):
            queue.put((acc + city[neighbor[0][1]][neighbor[0][0]], neighbor))

    raise Exception("No path found")


def part1(city: City) -> None:
    start = 0, 0
    end = len(city[0]) - 1, len(city) - 1
    result = dijkstra(city, start, end)
    print("Part 1:", result)


def part2(city: City) -> None:
    start = 0, 0
    end = len(city[0]) - 1, len(city) - 1
    result = dijkstra(city, start, end, min=4, max=10)
    print("Part 2:", result)


def main(lines: List[str]) -> None:
    city = parse_input(lines)
    part1(city)
    part2(city)
