
def _estimate_optimal_partitions(output_size: int, index_size: int) -> int:
    """Estimate optimal number of partitions based on contention ratio."""
    # Safety check for edge cases
    if output_size == 0 or index_size == 0:
        return _get_min_partitions()

    contention_ratio = index_size / output_size

    # Size-aware partition limits (larger tensors = fewer partitions to limit memory)
    max_partitions_for_size = _get_max_partitions_for_size(output_size)

    # Contention-based calculation - square root scaling
    # Use max to ensure we never go below min_partitions for the base calculation
    base_partitions = max(_get_min_partitions(), int(math.sqrt(contention_ratio) * 16))

    # Round to power of 2 and apply limits
    partitions = 2 ** math.ceil(math.log2(base_partitions))
    return min(partitions, max_partitions_for_size, _get_max_partitions())

