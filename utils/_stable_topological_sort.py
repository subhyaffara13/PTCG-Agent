
def _stable_topological_sort(
    graph: torch.fx.Graph,
    node_to_additional_deps: dict[Node, OrderedSet[Node]],
) -> None:
    assert _stable_topological_sort_impl(graph, node_to_additional_deps)

