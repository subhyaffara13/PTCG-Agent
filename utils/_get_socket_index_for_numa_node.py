
def _get_socket_index_for_numa_node(*, numa_node_index: int) -> int:
    arbitrary_cpu_index = _get_arbitrary_allowed_cpu_index_for_numa_node(
        numa_node_index=numa_node_index
    )

    return _get_socket_index_for_cpu(cpu_index=arbitrary_cpu_index)

