
def _boundaries_helper(tb: TensorBox) -> tuple[str, sympy.Expr, sympy.Expr, sympy.Expr]:
    # Calculate the maximum offset for the boundaries tensor
    # For a strided tensor, this is sum((size[i] - 1) * stride[i]) + stride[-1]
    # This ensures the mask check in bucketize_binary_search works correctly
    # for both contiguous and non-contiguous tensors.
    size = tb.get_size()
    stride = tb.get_stride()
    max_offset = sum((s - 1) * st for s, st in zip(size, stride)) + stride[-1]
    return (
        tb.get_name(),
        size[-1],
        max_offset,
        stride[-1],
    )

