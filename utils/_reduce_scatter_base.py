
def _reduce_scatter_base(
    output, input, op=ReduceOp.SUM, group=None, async_op: bool = False
):
    """
    Reduces, then scatters a flattened tensor to all processes in a group.

    Args:
        output (Tensor): Output tensor.
        input (Tensor): Input tensor that is of size output tensor size times world size
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group.

    .. warning::
        `_reduce_scatter_base` is a private function. Users should use
        `reduce_scatter_tensor` instead.

    """
    return reduce_scatter_tensor(output, input, op, group, async_op)

