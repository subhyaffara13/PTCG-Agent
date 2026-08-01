
def contiguous_last_dim(x):
    """Ensure that realized IR node has a contiguous stride in the last dimension."""
    strides = x.maybe_get_stride()
    if strides and strides[-1] != 1:
        contiguous_stride_order = list(reversed(range(len(x.get_size()))))
        return ExternKernel.require_stride_order(x, contiguous_stride_order)
    return x

