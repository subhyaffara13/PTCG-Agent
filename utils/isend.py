
def isend(
    tensor: torch.Tensor,
    dst: int | None = None,
    group: ProcessGroup | None = None,
    tag: int = 0,
    group_dst: int | None = None,
) -> Work | None:
    """
    Send a tensor asynchronously.

    .. warning::
        Modifying ``tensor`` before the request completes causes undefined
        behavior.

    .. warning::
        ``tag`` is not supported with the NCCL backend.

    Unlike send, which is blocking, isend allows src == dst rank, i.e. send to self.

    Args:
        tensor (Tensor): Tensor to send.
        dst (int): Destination rank on global process group (regardless of ``group`` argument)
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        tag (int, optional): Tag to match send with remote recv
        group_dst (int, optional): Destination rank on ``group``.  Invalid to specify both ``dst`` and ``group_dst``

    Returns:
        A distributed request object.
        None, if not part of the group

    """
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            isend,
            relevant_args,
            tensor,
            dst=dst,
            group=group,
            tag=tag,
            group_dst=group_dst,
        )

    group = _group_or_default_group(group)
    group_dst = _canonicalize_group_rank(group, dst, group_dst)
    _check_single_tensor(tensor, "tensor")
    if _rank_not_in_group(group):
        _warn_not_in_group("isend")
        return None

    if tensor.is_complex():
        tensor = torch.view_as_real(tensor)

    return group.send([tensor], group_dst, tag)

