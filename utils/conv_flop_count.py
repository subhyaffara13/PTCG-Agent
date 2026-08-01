
def conv_flop_count(
    x_shape: list[int],
    w_shape: list[int],
    out_shape: list[int],
    transposed: bool = False,
) -> int:
    """Count flops for convolution.

    Note only multiplication is
    counted. Computation for bias are ignored.
    Flops for a transposed convolution are calculated as
    flops = (x_shape[2:] * prod(w_shape) * batch_size).
    Args:
        x_shape (list(int)): The input shape before convolution.
        w_shape (list(int)): The filter shape.
        out_shape (list(int)): The output shape after convolution.
        transposed (bool): is the convolution transposed
    Returns:
        int: the number of flops
    """
    batch_size = x_shape[0]
    conv_shape = (x_shape if transposed else out_shape)[2:]
    c_out, c_in, *filter_size = w_shape

    """
    General idea here is that for a regular conv, for each point in the output
    spatial dimension we convolve the filter with something (hence
    `prod(conv_shape) * prod(filter_size)` ops). Then, this gets multiplied by
    1. batch_size, 2. the cross product of input and weight channels.

    For the transpose, it's not each point in the *output* spatial dimension but
    each point in the *input* spatial dimension.
    """
    # NB(chilli): I don't think this properly accounts for padding :think:
    # NB(chilli): Should be 2 * c_in - 1 technically for FLOPs.
    flop = prod(conv_shape) * prod(filter_size) * batch_size * c_out * c_in * 2
    return flop

