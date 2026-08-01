
def _scaled_mm_flop(
    a_shape,
    b_shape,
    scale_a_shape,
    scale_b_shape,
    bias_shape=None,
    scale_result_shape=None,
    out_dtype=None,
    use_fast_accum=False,
    out_shape=None,
    **kwargs,
) -> int:
    """Count flops for _scaled_mm."""
    return mm_flop(a_shape, b_shape)

