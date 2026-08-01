
def baddbmm_flop(self_shape, a_shape, b_shape, out_shape=None, **kwargs) -> int:
    """Count flops for the baddbmm operation."""
    # Inputs should be a list of length 3.
    # Inputs contains the shapes of three tensors.
    return bmm_flop(a_shape, b_shape)

