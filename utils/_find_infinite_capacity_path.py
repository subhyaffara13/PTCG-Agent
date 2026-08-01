
def _find_infinite_capacity_path(
    nx_graph: nx.DiGraph[str, dict[str, Any]],
) -> list[tuple[str, str, str]] | None:
    """BFS from source to sink following only infinite-capacity edges.

    Returns a list of (from_node, to_node, reason) tuples representing the path,
    or None if no such path exists.
    """

    visited = OrderedSet(["source"])
    # Each queue item: (current_node, path_of_edges)
    # where path_of_edges is a list of (from_node, to_node, reason) tuples
    queue: deque[tuple[str, list[tuple[str, str, str]]]] = deque([("source", [])])

    while queue:
        node, edge_path = queue.popleft()
        for neighbor in nx_graph.successors(node):
            if neighbor in visited:
                continue
            edge_data = nx_graph[node][neighbor]
            capacity = edge_data.get("capacity", 0)
            # Check for infinite capacity (either math.inf or INT_INF)
            if capacity == math.inf or capacity == INT_INF:
                reason = edge_data.get("reason", "unknown")
                new_edge = (node, neighbor, reason)
                new_path = edge_path + [new_edge]
                if neighbor == "sink":
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    return None

