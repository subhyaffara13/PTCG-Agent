
def _get_logical_cpus_to_bind_to(
    *,
    gpu_index: int,
    numa_options: NumaOptions,
) -> set[int]:
    """
    Args:
        gpu_index: The index of the GPU that will be used by the subprocess.
            Example: 0
        numa_options: See NumaOptions for details.

    Returns:
        Set of logical CPU indices to bind to.
    """
    if numa_options.affinity_mode == AffinityMode.NODE:
        logical_cpus = _node_get_logical_cpus_to_bind_to(gpu_index=gpu_index)
    elif numa_options.affinity_mode == AffinityMode.SOCKET:
        logical_cpus = _socket_get_logical_cpus_to_bind_to(gpu_index=gpu_index)
    elif numa_options.affinity_mode == AffinityMode.EXCLUSIVE:
        logical_cpus = _exclusive_get_logical_cpus_to_bind_to(gpu_index=gpu_index)
    elif numa_options.affinity_mode == AffinityMode.CORE_COMPLEX:
        logical_cpus = _core_complex_get_logical_cpus_to_bind_to(gpu_index=gpu_index)
    else:
        raise ValueError(f"Affinity mode {numa_options.affinity_mode} not supported.")

    return logical_cpus

