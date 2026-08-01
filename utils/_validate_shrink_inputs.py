
def _validate_shrink_inputs(ranks_to_exclude: list[int], shrink_flags: int) -> None:
    """Validate input parameters for shrink_group."""
    if not isinstance(ranks_to_exclude, list):
        raise TypeError(
            f"ranks_to_exclude must be a list, but got {type(ranks_to_exclude).__name__}. "
            f"Example: [1, 3, 5] to exclude ranks 1, 3, and 5."
        )

    if not ranks_to_exclude:
        raise ValueError(
            "ranks_to_exclude cannot be empty. To shrink a group, you must specify at least "
            "one rank to exclude. Example: [failed_rank_id]"
        )

    # Validate shrink_flags with clear explanation of valid values
    valid_flags = [SHRINK_DEFAULT, SHRINK_ABORT]
    if not isinstance(shrink_flags, int) or shrink_flags not in valid_flags:
        raise ValueError(
            f"Invalid shrink_flags value: {shrink_flags}. Must be one of: "
            f"SHRINK_DEFAULT ({SHRINK_DEFAULT}) or SHRINK_ABORT ({SHRINK_ABORT}). "
            f"Use SHRINK_ABORT to abort ongoing operations before shrinking."
        )

