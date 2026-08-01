
def _get_remote_tensors_default(
    local: torch.Tensor, group_name: c10d.GroupName
) -> tuple[torch.Tensor, ...]:
    hdl = rendezvous(local, group_name)
    if hdl is None:
        raise ValueError("Tensor is not allocated from Symmetric Memory")

    return tuple(
        hdl.get_remote_tensor(peer, local.size(), local.dtype)
        for peer in range(hdl.world_size)
    )

