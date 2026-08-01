
def collect_node_descendants(
    graph: torch.fx.Graph,
) -> dict[torch.fx.Node, OrderedSet[torch.fx.Node]]:
    """
    Collects the descendants of each node in the graph.
    Args:
        graph (torch.fx.Graph): The graph to collect descendants from.
    Returns:
        dict[torch.fx.Node, OrderedSet[torch.fx.Node]]: A dictionary mapping each node to its descendants.
    """
    node_descendants: dict[torch.fx.Node, OrderedSet[torch.fx.Node]] = (
        collections.defaultdict(OrderedSet)
    )
    outdegree = collections.defaultdict(int)
    queue = []

    for node in graph.nodes:
        n_outdegree = len(node.users)
        if n_outdegree == 0:
            queue.append(node)
        else:
            outdegree[node] = len(node.users)

    while queue:
        node = queue.pop()
        for input_node in node.all_input_nodes:
            node_descendants[input_node] |= node_descendants[node]
            node_descendants[input_node].add(node)
            outdegree[input_node] -= 1

            if outdegree[input_node] == 0:
                queue.append(input_node)

    return node_descendants

