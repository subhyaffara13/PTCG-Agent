
def bmm_flop(a_shape, b_shape, out_shape=None, **kwargs) -> int:
    """Count flops for the bmm operation."""
    # Inputs should be a list of length 2.
    # Inputs contains the shapes of two tensor.
    b, m, k = a_shape
    b2, k2, n = b_shape
    if b != b2:
        raise AssertionError(f"bmm: batch dimensions must match (b == b2), got {b} and {b2}")
    if k != k2:
        raise AssertionError(f"bmm: inner dimensions must match (k == k2), got {k} and {k2}")
    # NB(chilli): Should be 2 * k - 1 technically for FLOPs.
    flop = b * m * n * 2 * k
    return flop

