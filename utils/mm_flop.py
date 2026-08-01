
def mm_flop(a_shape, b_shape, *args, out_shape=None, **kwargs) -> int:
    """Count flops for matmul."""
    # Inputs should be a list of length 2.
    # Inputs contains the shapes of two matrices.
    m, k = a_shape
    k2, n = b_shape
    if k != k2:
        raise AssertionError(f"matmul: inner dimensions must match (k == k2), got {k} and {k2}")
    # NB(chilli): Should be 2 * k - 1 technically for FLOPs.
    return m * n * 2 * k

