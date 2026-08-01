
def validate_exclusive_idx(rank: int, ex_idx: int):
    """
    Validates that ex_idx is a valid exclusive index
    for the given shape.
    """

    if not isinstance(ex_idx, Dim):
        raise AssertionError(f"ex_idx must be Dim, got {type(ex_idx)}")
    if not isinstance(rank, Dim):
        raise AssertionError(f"rank must be Dim, got {type(rank)}")
    if not (ex_idx > 0 and ex_idx <= rank):
        raise AssertionError(
            f"ex_idx {ex_idx} is out of bounds for rank {rank} (must be in (0, rank])"
        )

