
def all_reduce_inplace(
    tensor: torch.Tensor,
    op: str = "sum",
    group=None,
    async_op: bool = False,
    tag: str = "",
):
    if async_op:
        raise AssertionError(
            "Can't remap async version of inplace op to functional collective"
        )

    group = group or dist.group.WORLD
    if group is None:
        raise AssertionError("group cannot be None")

    return tensor.copy_(all_reduce(tensor, op, group, tag))

