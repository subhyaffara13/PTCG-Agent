
def get_symm_mem_workspace(
    group_name: c10d.GroupName, min_size: int
) -> _SymmetricMemory:
    """
    Get the symmetric memory workspace associated with the process group. If
    ``min_size`` is greater than the workspace associated with ``group_name``,
    the workspace will be re-allocated and re-rendezvous'd.

    Args:
        group_name (str): the name of the process group.
        min_size (int): the size requirement for the workspace in bytes.

    Returns:
        _SymmetricMemory: the symmetric memory workspace associated with the
        group.
    """
    tensor = _group_name_to_workspace_tensor.get(group_name)
    size = tensor.numel() * tensor.element_size() if tensor is not None else 0
    if tensor is None or size < min_size:
        if torch.cuda.is_current_stream_capturing():
            curr_size = 0 if tensor is None else tensor.numel() * tensor.element_size()
            raise RuntimeError(
                f"get_symm_mem_workspace(): the requested size ({min_size} bytes) "
                "is greater than the size of the currently allocated workspace "
                f"({curr_size} bytes). It's currently not possible to expand the "
                "workspace size during graph capture. Please invoke "
                f'`get_symm_mem_workspace(group_name="{group_name}", '
                f'min_size="{min_size}")` before initiating the graph capture '
                "and try again."
            )
        tensor = _SymmetricMemory.empty_strided_p2p(
            (max(size, min_size),),
            [1],
            torch.uint8,
            torch.device(f"cuda:{torch.cuda.current_device()}"),
            group_name,
        )
        _group_name_to_workspace_tensor[group_name] = tensor
    return _SymmetricMemory.rendezvous(tensor)

