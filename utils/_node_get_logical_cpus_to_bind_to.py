
def _node_get_logical_cpus_to_bind_to(*, gpu_index: int) -> set[int]:
    """
    Core logic of 'node' numa strategy.
    """
    numa_node_index = _get_numa_node_index_for_gpu_index(gpu_index=gpu_index)

    return _get_allowed_logical_cpu_indices_for_numa_node(
        numa_node_index=numa_node_index
    )

