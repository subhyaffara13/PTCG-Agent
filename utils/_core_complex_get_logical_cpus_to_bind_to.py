
def _core_complex_get_logical_cpus_to_bind_to(*, gpu_index: int) -> set[int]:
    """
    Core logic of 'core-complex' numa strategy.

    Each GPU is assigned a full core complex (group of cores sharing L3 cache)
    within its affined NUMA node.
    """
    numa_node_index = _get_numa_node_index_for_gpu_index(gpu_index=gpu_index)

    gpu_indices = _get_gpu_indices_for_numa_node(numa_node_index=numa_node_index)
    gpu_indices = sorted(gpu_indices)
    original_gpu_relative_index = gpu_indices.index(gpu_index)

    allowed_logical_cpu_indices = _get_allowed_logical_cpu_indices_for_numa_node(
        numa_node_index=numa_node_index
    )

    # Arbitrarily use the min logical cpu index on the max level cache
    # to represent the max level cache.
    max_level_cache_to_allowed_logical_cpu_indices = _group_by(
        allowed_logical_cpu_indices,
        lambda logical_cpu_index: min(
            _get_logical_cpus_sharing_same_max_level_cache_as(
                logical_cpu_index=logical_cpu_index
            )
        ),
    )

    max_level_cache_to_allowed_logical_cpu_indices = dict(
        sorted(
            max_level_cache_to_allowed_logical_cpu_indices.items(),
            # First, prioritize caches with more available cpus
            # Second, prioritize lower index cpus (just for clarity/consistency)
            key=lambda item: (-len(item[1]), item[0]),
        )
    )

    cache_index_for_original_gpu = original_gpu_relative_index % len(
        max_level_cache_to_allowed_logical_cpu_indices
    )
    logical_cpu_indices_for_original_gpu = list(
        max_level_cache_to_allowed_logical_cpu_indices.values()
    )[cache_index_for_original_gpu]

    return logical_cpu_indices_for_original_gpu

