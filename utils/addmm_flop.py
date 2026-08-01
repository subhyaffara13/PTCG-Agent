
def addmm_flop(self_shape, a_shape, b_shape, out_shape=None, **kwargs) -> int:
    """Count flops for addmm."""
    return mm_flop(a_shape, b_shape)

