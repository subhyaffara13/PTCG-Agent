
def _get_allowed_logical_cpu_indices_for_numa_node(*, numa_node_index: int) -> set[int]:
    all_cpu_indices = _get_cpu_indices_for_numa_node_MAYBE_NOT_ALLOWED(
        numa_node_index=numa_node_index
    )
    allowed_cpu_indices = _get_allowed_cpu_indices_for_current_thread()
    return all_cpu_indices & allowed_cpu_indices

