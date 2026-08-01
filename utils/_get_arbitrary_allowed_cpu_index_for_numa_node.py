
def _get_arbitrary_allowed_cpu_index_for_numa_node(*, numa_node_index: int) -> int:
    return min(
        _get_allowed_logical_cpu_indices_for_numa_node(numa_node_index=numa_node_index)
    )

