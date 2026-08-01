
def _partial_needs_reduce_for_dtype_cast(
    reduce_op: str,
    src_dtype: torch.dtype,
    target_dtype: torch.dtype | None,
) -> bool:
    """Return True when reduce_op does not commute with the dtype cast."""
    if target_dtype is None or src_dtype == target_dtype:
        return False
    if target_dtype == torch.bool:
        return True
    if reduce_op in ("max", "min"):
        return False
    return src_dtype.is_floating_point and not target_dtype.is_floating_point

