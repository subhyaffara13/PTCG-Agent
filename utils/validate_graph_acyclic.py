
def validate_graph_acyclic(nodes: list[BaseSchedulerNode]) -> None:
    """
    Validate that the graph is acyclic by checking predecessor relationships.

    Raises:
        RuntimeError: If a cycle is detected in the graph
    """
    # DFS coloring scheme for cycle detection:
    # WHITE (0): Node has not been visited yet
    # GRAY (1): Node is currently being processed (in the recursion stack)
    # BLACK (2): Node has been completely processed (finished exploring all its predecessors)
    # A back edge (cycle) is detected when we encounter a GRAY node during DFS traversal
    WHITE, GRAY, BLACK = 0, 1, 2
    color = dict.fromkeys(nodes, WHITE)
    path: list[BaseSchedulerNode] = []  # Track current DFS path

    def dfs_visit(node: BaseSchedulerNode) -> None:
        if color[node] == BLACK:
            return

        if color[node] == GRAY:
            path.append(node)
            path_info = " -> ".join([node.get_name() for node in path])

            raise RuntimeError(
                f"Cycle detected in memory planning graph"
                f"Path containing cycle (i -> j: j is a dependency of i): {path_info} "
                f"This indicates invalid dependency relationships in the scheduler graph"
            )

        color[node] = GRAY
        path.append(node)

        for pred_node in node.mpi_node.pred_nodes:
            assert pred_node != node
            dfs_visit(pred_node)

        path.pop()
        color[node] = BLACK

    # Start DFS from all unvisited nodes
    for node in nodes:
        if color[node] == WHITE:
            dfs_visit(node)

