
def _get_validated_logical_cpus_to_bind_to(
    *,
    gpu_index: int,
    numa_options: NumaOptions,
) -> set[int]:
    logical_cpu_indices = _get_logical_cpus_to_bind_to(
        gpu_index=gpu_index, numa_options=numa_options
    )
    _raise_if_binding_invalid(logical_cpu_indices=logical_cpu_indices)

    return logical_cpu_indices

