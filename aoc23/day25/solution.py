from typing import List

import networkx as nx  # type: ignore


def parse_input(lines: List[str]) -> nx.Graph:
    graph = nx.Graph()
    for line in lines:
        component, connections_str = line.strip().split(": ")
        connections = set(connections_str.split(" "))
        # Add connections to this component
        graph.add_edges_from([(component, connection) for connection in connections])

    return graph


def part1(graph: nx.Graph) -> None:
    # Get the minimum edge cut
    edges = nx.minimum_edge_cut(graph)
    # Remove the edges from the graph
    graph.remove_edges_from(edges)
    # Assert we have 2 connected components
    assert nx.number_connected_components(graph) == 2
    # Get the size of both components
    connected_components = list(nx.connected_components(graph))
    c1 = len(connected_components[0])
    c2 = len(connected_components[1])
    print("Part 1:", c1 * c2)


def main(lines: List[str]) -> None:
    graph = parse_input(lines)
    part1(graph)
