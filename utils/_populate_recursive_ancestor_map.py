
def _populate_recursive_ancestor_map(graph: torch.fx.Graph) -> dict[Node, set[Node]]:
    node_to_recursive_ancestors: dict[Node, set[Node]] = {}
    for node in graph.nodes:
        node_to_recursive_ancestors[node] = set()
    for node in graph.nodes:
        all_args = _get_flat_args_unique(node, {})
        for arg in all_args:
            if isinstance(arg, Node):
                node_to_recursive_ancestors[node].update(
                    node_to_recursive_ancestors[arg]
                )
                node_to_recursive_ancestors[node].add(arg)
    return node_to_recursive_ancestors

