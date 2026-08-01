
def _populate_additional_deps(
    graph: torch.fx.Graph, node_to_mutated_arg_positions: dict[Node, OrderedSet[int]]
) -> dict[Node, OrderedSet[Node]]:
    node_to_additional_deps: dict[Node, OrderedSet[Node]] = defaultdict(OrderedSet)
    _add_mutation_dependencies(node_to_mutated_arg_positions, node_to_additional_deps)
    _add_global_state_dependencies(graph, node_to_additional_deps)
    return node_to_additional_deps

