
def _dtensor_repr(x):
    """Return a stable string representation for a DTensor-like object."""
    if _is_rank_zero():
        return f"DTensor (rank0) -> {repr(x._local_tensor)}"
    return "DTensor(non-rank0)"

