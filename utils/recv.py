
def recv(
    tensor: torch.Tensor,
    src: int | None = None,
    group: ProcessGroup | None = None,
    tag: int = 0,
    group_src: int | None = None,
) -> int:
    """
    Receives a tensor synchronously.

    .. warning::
        ``tag`` is not supported with the NCCL backend.

    Args:
        tensor (Tensor): Tensor to fill with received data.
        src (int, optional): Source rank on global process group (regardless of ``group`` argument).
            Will receive from any process if unspecified.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        tag (int, optional): Tag to match recv with remote send
        group_src (int, optional): Destination rank on ``group``.  Invalid to specify both ``src`` and ``group_src``.

    Returns:
        Sender rank
        -1, if not part of the group

    """
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            recv,
            relevant_args,
            tensor,
            src=src,
            group=group,
            tag=tag,
            group_src=group_src,
        )

    work = irecv(tensor, src=src, group=group, tag=tag, group_src=group_src)
    if work is None:
        return -1
    work.wait()
    if src is None:
        if group_src is None:
            group_src = work._source_rank()
        group = _group_or_default_group(group)
        _check_not_self_rank(group, group_src, "source")
        src = get_global_rank(group, group_src)
    return src


def recv(result: _Sequence[_ods_ir.Type], token: _ods_ir.Value, channel_handle: _Union[_Any, _ods_ir.Attribute], *, is_host_transfer: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, source_target_pairs: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, RecvOp]:
  op = RecvOp(result=result, token=token, channel_handle=channel_handle, is_host_transfer=is_host_transfer, source_target_pairs=source_target_pairs, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def recv(result: _Sequence[_ods_ir.Type], token: _ods_ir.Value, channel_handle: _Union[_Any, _ods_ir.Attribute], *, is_host_transfer: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, source_target_pairs: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, RecvOp]:
  op = RecvOp(result=result, token=token, channel_handle=channel_handle, is_host_transfer=is_host_transfer, source_target_pairs=source_target_pairs, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

