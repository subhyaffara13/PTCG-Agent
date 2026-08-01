
def _low_contention_all_gather_meta(
    tensor: torch.Tensor,
    group_name: c10d.GroupName,
) -> torch.Tensor:
    group_size = c10d._get_group_size_by_name(group_name)
    return tensor.new_empty(tensor.shape[0] * group_size, *tensor.shape[1:])

