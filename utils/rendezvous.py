
def rendezvous(url: str, rank: int = -1, world_size: int = -1, **kwargs):
    if not isinstance(url, (str, bytes)):
        raise RuntimeError(f"`url` must be a string. {type(url)}: {url}")

    if not isinstance(rank, numbers.Integral):
        raise RuntimeError(f"`rank` must be an integer. {rank}")

    if not isinstance(world_size, numbers.Integral):
        raise RuntimeError(f"`world_size` must be an integer. {world_size}")

    return _rendezvous_helper(url, rank, world_size, **kwargs)


def rendezvous(
    tensor: torch.Tensor, group: c10d.GroupName | ProcessGroup
) -> _SymmetricMemory:
    r"""
    rendezvous(tensor, group) -> _SymmetricMemory

    Establish a symmetric memory tensor among participating processes. This is
    a collective operation.

    Args:
        tensor (:class:`torch.Tensor`): the local tensor used to establish the symmetric memory tensor.
            It must be allocated via :func:`torch._distributed._symmetric_memory.empty()`. The shape,
            dtype, and device type must be identical across all participating processes.
        group (Union[str, :class:`torch.distributed.ProcessGroup`]): The group identifying the
            participating processes. This can be either a group name or a process group object.
    """
    from torch._C._distributed_c10d import ProcessGroup

    if isinstance(group, str):
        group_name = c10d.GroupName(group)
    elif isinstance(group, ProcessGroup):
        group_name = group.group_name
    else:
        raise TypeError(f"rendezvous: unsupported group type: {type(group)}")

    return _SymmetricMemory.rendezvous(tensor, group_name)

