
def _get_unexposed_collectives(graph: torch.fx.Graph) -> list[torch.fx.Node]:
    """
    Find all unexposed collectives in the graph.

    Because we don't have the runtime estimate, this function is a rough
    estimation using the following strong/hand-wavy assumptions:

    - Only a predefined set of "compute intensive" operation can hide a collective.
    - Any "compute intensive" operation can hide exactly one collective.
    """

    def _is_compute_intensive(node: torch.fx.Node) -> bool:
        return node.target is torch.ops.aten.mm.default

    collective_to_overlapping_candidates = defaultdict(list)
    available_nodes = OrderedSet[torch.fx.Node]()
    collective_to_overlappable_nodes = _get_collective_to_overlappable_nodes(graph)
    for collective, overlappable_nodes in collective_to_overlappable_nodes.items():
        candidates = [x for x in overlappable_nodes if _is_compute_intensive(x)]
        collective_to_overlapping_candidates[collective] = candidates
        available_nodes.update(candidates)

    unexposed_collectives = []
    for (
        collective,
        overlapping_candidates,
    ) in collective_to_overlapping_candidates.items():
        # Each collective consumes exactly one overlapping candidate
        for x in overlapping_candidates:
            if x in available_nodes:
                unexposed_collectives.append(collective)
                available_nodes.remove(x)
                break
    return unexposed_collectives

