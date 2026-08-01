
def reduce_scatter_tensor_inplace(
    output: torch.Tensor,
    input: torch.Tensor,
    op: str = "sum",  # TODO type is actually c10d ReduceOp. is this ok?
    group=None,  # TODO add a type
    async_op: bool = False,
    scatter_dim: int = 0,
    tag: str = "",
):
    if async_op:
        raise AssertionError(
            "Can't remap async version of inplace op to functional collective"
        )

    group = group or dist.group.WORLD
    if group is None:
        raise AssertionError("group cannot be None")

    return output.copy_(reduce_scatter_tensor(input, op, scatter_dim, group, tag))

