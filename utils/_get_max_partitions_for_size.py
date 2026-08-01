
def _get_max_partitions_for_size(output_size: int) -> int:
    """
    Get maximum partitions based on output tensor size.

    Larger tensors use fewer partitions to limit memory overhead.
    """
    if output_size >= 100_000_000:  # >= 100M elements
        return 4
    elif output_size >= 10_000_000:  # >= 10M elements
        return 8
    elif output_size >= 1_000_000:  # >= 1M elements
        return 16
    else:  # < 1M elements
        return _get_max_partitions()

