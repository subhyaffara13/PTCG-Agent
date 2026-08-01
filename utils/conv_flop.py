
def conv_flop(x_shape, w_shape, _bias, _stride, _padding, _dilation, transposed, *args, out_shape=None, **kwargs) -> int:
    """Count flops for convolution."""
    # pyrefly: ignore [bad-argument-type]
    return conv_flop_count(x_shape, w_shape, out_shape, transposed=transposed)

