
def irecv(
    tensor: torch.Tensor,
    src: int | None = None,
    group: ProcessGroup | None = None,
    tag: int = 0,
    group_src: int | None = None,
) -> Work | None:
    """
    Receives a tensor asynchronously.

    .. warning::
        ``tag`` is not supported with the NCCL backend.

    Unlike recv, which is blocking, irecv allows src == dst rank, i.e. recv from self.

    Args:
        tensor (Tensor): Tensor to fill with received data.
        src (int, optional): Source rank on global process group (regardless of ``group`` argument).
            Will receive from any process if unspecified.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        tag (int, optional): Tag to match recv with remote send
        group_src (int, optional): Destination rank on ``group``.  Invalid to specify both ``src`` and ``group_src``.

    Returns:
        A distributed request object.
        None, if not part of the group

    """
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            irecv,
            relevant_args,
            tensor,
            src=src,
            group=group,
            tag=tag,
            group_src=group_src,
        )

    _check_single_tensor(tensor, "tensor")
    if _rank_not_in_group(group):
        _warn_not_in_group("irecv")
        return None

    if tensor.is_complex():
        tensor = torch.view_as_real(tensor)

    group = _group_or_default_group(group)
    if src is None and group_src is None:
        return group.recv_anysource([tensor], tag)
    else:
        group_src = _canonicalize_group_rank(group, src, group_src)
        return group.recv([tensor], group_src, tag)

