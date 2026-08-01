
def online_softmax_combine(lhs_max, lhs_sum, rhs_max, use_fast_math: tl.constexpr):
    """
    When we do combine, we assume lhs is the accumulator and rhs is the next
    block of data.
    Then rhs_sum is always 1. With that assumption, we can save some registers
    and computation.
    """
    out_max = maximum(lhs_max, rhs_max)

    lhs_scale = tl.where(
        out_max == float("-inf"), 1.0, exp(lhs_max - out_max, use_fast_math)
    )
    rhs_scale = tl.where(
        out_max == float("-inf"), 1.0, exp(rhs_max - out_max, use_fast_math)
    )

    # Should be
    #   out_sum = lhs_sum * lhs_scale + rhs_sum * rhs_scale
    # but since rhs_sum is all 1, we can simplify it.
    out_sum = lhs_sum * lhs_scale + rhs_scale
    return out_max, out_sum

