
def send(connection: IPCBase, data: Any) -> None:
    """Send data to a connection encoded and framed.

    The data must be JSON-serializable. We assume that a single send call is a
    single frame to be sent on the connect.
    """
    connection.write(json.dumps(data))


def send(connection: IPCBase, data: IPCMessage) -> None:
    """Send data to a connection encoded and framed.

    The data must be a non-abstract IPCMessage. We assume that a single send call is a
    single frame to be sent.
    """
    buf = WriteBuffer()
    data.write(buf)
    connection.write_bytes(buf.getvalue())


def send(
    tensor: torch.Tensor,
    dst: int | None = None,
    group: ProcessGroup | None = None,
    tag: int = 0,
    group_dst: int | None = None,
) -> None:
    """
    Send a tensor synchronously.

    .. warning::
        ``tag`` is not supported with the NCCL backend.

    Args:
        tensor (Tensor): Tensor to send.
        dst (int): Destination rank on global process group (regardless of ``group`` argument).
            Destination rank should not be the same as the rank of the current process.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        tag (int, optional): Tag to match send with remote recv
        group_dst (int, optional): Destination rank on ``group``.  Invalid to specify both ``dst`` and ``group_dst``.

    """
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            send,
            relevant_args,
            tensor,
            dst=dst,
            group=group,
            tag=tag,
            group_dst=group_dst,
        )

    group = _group_or_default_group(group)
    group_dst = _canonicalize_group_rank(group, dst, group_dst)
    _check_not_self_rank(group, group_dst, "destination")
    work = isend(tensor, group=group, tag=tag, group_dst=group_dst)
    if work is not None:
        work.wait()


def send(inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], token: _ods_ir.Value, channel_handle: _Union[_Any, _ods_ir.Attribute], *, is_host_transfer: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, source_target_pairs: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SendOp(inputs=inputs, token=token, channel_handle=channel_handle, is_host_transfer=is_host_transfer, source_target_pairs=source_target_pairs, results=results, loc=loc, ip=ip).result


def send(inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], token: _ods_ir.Value, channel_handle: _Union[_Any, _ods_ir.Attribute], *, is_host_transfer: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, source_target_pairs: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SendOp(inputs=inputs, token=token, channel_handle=channel_handle, is_host_transfer=is_host_transfer, source_target_pairs=source_target_pairs, results=results, loc=loc, ip=ip).result

