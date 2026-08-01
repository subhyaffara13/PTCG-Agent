
def _exclusive_get_logical_cpus_to_bind_to(*, gpu_index: int) -> set[int]:
    """
    Core logic of 'exclusive' numa strategy.
    """
    numa_node_index = _get_numa_node_index_for_gpu_index(gpu_index=gpu_index)

    gpu_indices = _get_gpu_indices_for_numa_node(numa_node_index=numa_node_index)
    gpu_indices = sorted(gpu_indices)
    original_gpu_relative_index = gpu_indices.index(gpu_index)

    allowed_logical_cpu_indices = _get_allowed_logical_cpu_indices_for_numa_node(
        numa_node_index=numa_node_index
    )

    # Arbitrarily use the min logical cpu index on the physical core to
    # represent the physical core.
    physical_core_to_allowed_logical_cpu_indices = _group_by(
        allowed_logical_cpu_indices,
        lambda logical_cpu_index: min(
            _get_logical_cpu_indices_sharing_same_physical_core_as(
                logical_cpu_index=logical_cpu_index
            )
        ),
    )
    # Sort the dict for consistency (dicts maintain order in Python)
    physical_core_to_allowed_logical_cpu_indices = dict(
        sorted(physical_core_to_allowed_logical_cpu_indices.items())
    )

    num_physical_cores_per_gpu = len(
        physical_core_to_allowed_logical_cpu_indices
    ) // len(gpu_indices)
    # Often, the number of physical cores will not be perfectly divisible by the number
    # of GPUs. In those cases, give the lowest GPU indices an extra core
    num_gpus_to_give_one_extra_physical_core = len(
        physical_core_to_allowed_logical_cpu_indices
    ) % len(gpu_indices)

    if num_physical_cores_per_gpu < 1:
        raise RuntimeError(
            f"There are only {len(physical_core_to_allowed_logical_cpu_indices)} physical cores on {numa_node_index=},"
            + f" but there are {len(gpu_indices)} GPUs associated with this NUMA node."
        )

    # Compute slice indices for this GPU
    start = original_gpu_relative_index * num_physical_cores_per_gpu + min(
        original_gpu_relative_index, num_gpus_to_give_one_extra_physical_core
    )
    end = (
        start
        + num_physical_cores_per_gpu
        + (
            1
            if original_gpu_relative_index < num_gpus_to_give_one_extra_physical_core
            else 0
        )
    )

    # Slice and flatten the logical CPUs from the selected physical cores
    logical_cpu_indices_for_original_gpu = {
        logical_cpu_index
        for logical_cpu_indices in list(
            physical_core_to_allowed_logical_cpu_indices.values()
        )[start:end]
        for logical_cpu_index in logical_cpu_indices
    }

    return logical_cpu_indices_for_original_gpu

