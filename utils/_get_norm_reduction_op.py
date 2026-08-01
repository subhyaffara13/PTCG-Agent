
def _get_norm_reduction_op(norm_type: int | float | str) -> ReductionOpType:
    """Get the reduction op for vector/foreach norm based on norm_type.

    For inf/-inf norms, returns simple reduction ops ("max", "min").
    For other norms (including 0), returns NormReduction which produces the
    appropriate Partial placement via get_placement_from_reduction_op.
    """
    if norm_type in (float("inf"), "inf"):
        return "max"
    elif norm_type in (float("-inf"), "-inf"):
        return "min"
    else:
        if not isinstance(norm_type, (int, float)):
            raise AssertionError
        return NormReduction(norm_type)

