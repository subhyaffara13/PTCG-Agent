
def _socket_get_logical_cpus_to_bind_to(*, gpu_index: int) -> set[int]:
    """
    Core logic of 'socket' numa strategy.
    """
    numa_node_index_of_gpu = _get_numa_node_index_for_gpu_index(gpu_index=gpu_index)
    socket_index = _get_socket_index_for_numa_node(
        numa_node_index=numa_node_index_of_gpu
    )
    numa_node_indices = _get_numa_node_indices_for_socket_index(
        socket_index=socket_index
    )

    logical_cpus = set()
    for numa_node_index in numa_node_indices:
        logical_cpus.update(
            _get_allowed_logical_cpu_indices_for_numa_node(
                numa_node_index=numa_node_index
            )
        )

    return logical_cpus

