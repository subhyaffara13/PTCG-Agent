
def _reduce_scatter_tensor(
    input: torch.Tensor,
    reduce_op: str,
    tag: str,
    ranks: list[int],
    group_size: int,
):
    group_name = c10d._resolve_group_name_by_ranks_and_tag(ranks, tag)
    return torch.ops._c10d_functional.reduce_scatter_tensor(
        input,
        reduce_op,
        group_size,
        group_name,
    )

