
def _get_cpu_indices_for_numa_node_MAYBE_NOT_ALLOWED(
    *, numa_node_index: int
) -> set[int]:
    """
    Returns:
        Indices of all CPUs associated with numa_node_index. However, the list
        is not filtered based on whether the thread is allowed to use them.
    """
    cpulist_absolute_path = f"/sys/devices/system/node/node{numa_node_index}/cpulist"
    try:
        with open(cpulist_absolute_path) as f:
            cpu_range_str = f.read()
    except FileNotFoundError as e:
        raise RuntimeError(
            f"Could not determine CPUs corresponding to {numa_node_index=}."
        ) from e
    return _get_set_of_int_from_ranges_str(cpu_range_str)

