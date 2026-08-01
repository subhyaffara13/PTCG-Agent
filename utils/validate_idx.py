
def validate_idx(rank: int, idx: int):
    """
    Validates that idx is a valid index for the given shape.
    Assumes the index is already canonicalized.
    """

    if not isinstance(idx, Dim):
        raise AssertionError(f"idx must be Dim, got {type(idx)}")
    if not isinstance(rank, Dim):
        raise AssertionError(f"rank must be Dim, got {type(rank)}")

    if not (idx >= 0 and idx < rank or idx == 0):
        raise AssertionError(f"idx {idx} is out of bounds for rank {rank}")

