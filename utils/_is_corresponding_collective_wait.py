
def _is_corresponding_collective_wait(
    collective_snode: BaseSchedulerNode,
    wait_snode: BaseSchedulerNode,
    node_output_sets: dict[BaseSchedulerNode, frozenset[str]],
    node_dep_sets: dict[BaseSchedulerNode, frozenset[str]],
) -> bool:
    """
    Check if a wait node corresponds to a given collective node.
    Uses pre-computed sets for O(1) lookup.
    """
    collective_outs = node_output_sets[collective_snode]
    unmet_deps = node_dep_sets[wait_snode]
    return bool(unmet_deps & collective_outs)

