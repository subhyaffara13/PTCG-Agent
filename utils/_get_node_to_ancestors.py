
def _get_node_to_ancestors(
    graph: torch.fx.Graph,
) -> dict[torch.fx.Node, OrderedSet[torch.fx.Node]]:
    """
    Compute the ancestors for all nodes in a graph.
    """
    node_to_ancestors = defaultdict(OrderedSet[torch.fx.Node])  # type: ignore[var-annotated]
    for node in graph.nodes:
        node_to_ancestors[node] = OrderedSet(node.all_input_nodes)
        for dep in node.all_input_nodes:
            node_to_ancestors[node] |= node_to_ancestors[dep]

    return node_to_ancestors

