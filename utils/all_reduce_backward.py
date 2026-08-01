
def all_reduce_backward(x, device_mesh):
    """Identity forward, all-reduce backward. Use before colwise layers."""
    return _AllReduceBackward.apply(x, device_mesh)


def all_reduce_backward(ctx, grad_output: torch.Tensor):
    """
    Backward for all_reduce: all_reduce with same reduce_op.
    Forward aggregates tensors, backward aggregates gradients.

    Args:
        ctx: Context object
        grad_output: Gradient from downstream operations

    Returns:
        Tuple of (grad_input, grad_group_name, grad_reduce_op)
        grad_group_name and grad_reduce_op are None (not differentiable)
    """
    group_name = ctx.group_name
    reduce_op = ctx.reduce_op

    if reduce_op != "sum":
        raise RuntimeError(
            f"all_reduce backward only supports 'sum' reduction, got '{reduce_op}'"
        )

    # Backward does all_reduce with the same reduce_op
    output = torch.ops._c10d_functional.all_reduce(
        grad_output.contiguous(), reduce_op, group_name
    )
    return wait_tensor(output), None, None

