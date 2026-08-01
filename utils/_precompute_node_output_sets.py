
def _precompute_node_output_sets(
    snodes: list[BaseSchedulerNode],
) -> dict[BaseSchedulerNode, OrderedSet[str]]:
    """
    Pre-compute output name sets for all nodes.

    This optimization avoids creating OrderedSet objects repeatedly during
    exposed time calculations.

    Returns:
        dict mapping each node to a set of its output names
    """
    return {
        snode: OrderedSet(o.get_name() for o in snode.get_outputs()) for snode in snodes
    }

