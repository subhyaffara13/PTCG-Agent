
def infer_dense_strides(
    size: Sequence[_IntLike],
    orig_strides: Sequence[_IntLike],
):
    """This is a mirror of the same function in aten/src/ATen/ExpandUtils.cpp

    Args:
        size: The size of the output tensor
        orig_strides: The strides of the input tensor
    Returns:
        List[int]: Dense non-overlapping strides that preserve the input tensor's layout permutation.
        The returned strides follow the same stride propagation rules as TensorIterator. This matches
        The behavior of empty_like()
    """
    fill_order = get_fill_order(orig_strides, V.graph.sizevars.shape_env)
    strides = construct_strides(size, fill_order)

    # Attention kernels require stride[-1]=1 for efficient memory access.
    # Ensure this by moving last dim to front of fill_order if needed.
    if strides[-1] != 1:
        last_dim = len(size) - 1
        fill_order = list(fill_order)
        fill_order.remove(last_dim)
        fill_order = [last_dim] + fill_order
        strides = construct_strides(size, fill_order)

    return strides

