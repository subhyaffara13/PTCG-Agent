
def _get_remote_tensors_meta(
    local: torch.Tensor, group_name: c10d.GroupName
) -> tuple[torch.Tensor, ...]:
    group = c10d._resolve_process_group(group_name)
    return tuple(torch.empty_like(local) for _ in range(group.size()))

