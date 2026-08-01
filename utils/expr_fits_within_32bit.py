
def expr_fits_within_32bit(e: sympy.Expr) -> bool:
    """Check if an expression fits within 32-bit integer range.

    NOTE: This function intentionally does not install guards. Callers are
    responsible for guarding (e.g. via check_leq) when they decide to use
    32-bit indexing based on this result.
    """
    from .virtualized import V

    int_max = torch.iinfo(torch.int32).max
    guarding_hint_or_throw = V.graph.sizevars.guarding_hint_or_throw
    has_guarding_hint = V.graph.sizevars.shape_env.has_guarding_hint

    if config.assume_32bit_indexing:
        V.graph.sizevars.check_leq(e, int_max)  # type: ignore[arg-type]
        return True

    # Allow for unhinted e as long as we can still statically prove
    # (e.g., via ValueRanges) that it is still in bounds
    if V.graph.sizevars.statically_known_true(e <= int_max):
        return True

    # AOTI doesn't guard on < 2**32, so checking hints isn't a viable option,
    # in case the hinted value is < 2**32, but the allowed range is larger.
    # However, to prevent possible perf regressions on pre-existing AOTI models
    # which don't set an upper bound on the valid range, we'll skip the check.
    # To recap:
    # - If using AOTI:
    #   - If allowed range has no upper bound, then check the hint to determine
    #       whether this fits in int32
    #   - If allowed range does have an upper bound, then obey the upper bound
    #       (check whether upper bound < int32_max) without checking the hint.

    if V.aot_compilation:
        # check whether value has an upper bound (1e20 is > INT64_MAX, assume
        # there is no upper bound if it can be larger than 1e20)
        if V.graph.sizevars.statically_known_true(e < 1e20):
            # if so, then assume int_max < upper bound < inf
            # so this could potentially have int64 values
            return False

    # Otherwise, the hint MUST exist and be in range
    return has_guarding_hint(e) and guarding_hint_or_throw(e) <= int_max

