
def _validate_and_process_excluded_ranks(
    ranks_to_exclude: list[int], group_info: dict
) -> set:
    """Validate excluded ranks and convert to set for efficient operations."""
    group_size = group_info["group_size"]
    current_rank = group_info["current_rank"]

    # Use set for O(1) duplicate detection and membership testing
    excluded_ranks_set = set()

    # Validate each rank with detailed error messages
    for i, rank in enumerate(ranks_to_exclude):
        if not isinstance(rank, int):
            raise TypeError(
                f"All elements in ranks_to_exclude must be integers. "
                f"Element at index {i} is {type(rank).__name__}: {rank}"
            )

        if not (0 <= rank < group_size):
            raise ValueError(
                f"Rank {rank} at index {i} is out of bounds for group size {group_size}. "
                f"Valid ranks are in range [0, {group_size - 1}]."
            )

        if rank in excluded_ranks_set:
            raise ValueError(
                f"Duplicate rank {rank} found in ranks_to_exclude at index {i}. "
                f"Each rank can only be excluded once."
            )

        excluded_ranks_set.add(rank)

    # Ensure we don't exclude all ranks
    if len(excluded_ranks_set) >= group_size:
        raise ValueError(
            f"Cannot exclude all {group_size} ranks from process group. "
            f"At least one rank must remain. Excluding {len(excluded_ranks_set)} ranks."
        )

    # Critical check: current rank should not be in excluded list
    if current_rank in excluded_ranks_set:
        raise RuntimeError(
            f"Current rank {current_rank} is in the exclusion list and should not call shrink_group(). "
            f"Only non-excluded ranks should participate in the shrinking operation. "
            f"Excluded ranks should terminate their processes instead."
        )

    return excluded_ranks_set

