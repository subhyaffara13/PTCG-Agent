
def _get_collective_to_overlappable_nodes(
    graph: torch.fx.Graph,
) -> dict[torch.fx.Node, list[torch.fx.Node]]:
    """
    For each collective in the graph, find nodes that are neither ancestors nor
    descendants of the collective.
    """

    def is_collective(node) -> bool:
        # Only consider all-gather and reduce-scatter in the context of
        # micro-pipeline TP.
        return node.target in [
            torch.ops._c10d_functional.all_gather_into_tensor.default,
            torch.ops._c10d_functional.reduce_scatter_tensor.default,
        ]

    node_to_ancestors = _get_node_to_ancestors(graph)
    collective_to_overlappable_nodes = defaultdict(list)
    for node in graph.nodes:
        if not is_collective(node):
            continue
        for x in graph.nodes:
            if (
                node not in node_to_ancestors[x]
                and x not in node_to_ancestors[node]
                and x.op == "call_function"
            ):
                collective_to_overlappable_nodes[node].append(x)

    return collective_to_overlappable_nodes

