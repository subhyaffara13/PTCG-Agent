
def _low_contention_reduce_scatter_meta(
    tensor: torch.Tensor,
    reduce_op: str,
    group_name: c10d.GroupName,
) -> torch.Tensor:
    group_size = c10d._get_group_size_by_name(group_name)
    return tensor.unflatten(0, (group_size, -1)).mean(dim=0)

