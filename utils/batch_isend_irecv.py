
def batch_isend_irecv(p2p_op_list: list[P2POp]) -> list[Work]:
    """
    Send or Receive a batch of tensors asynchronously and return a list of requests.

    Process each of the operations in ``p2p_op_list`` and return the corresponding
    requests. NCCL, Gloo, and UCC backend are currently supported.

    Args:
        p2p_op_list: A list of point-to-point operations(type of each operator is
            ``torch.distributed.P2POp``). The order of the isend/irecv in the list
            matters and it needs to match with corresponding isend/irecv on the
            remote end.

    Returns:
        A list of distributed request objects returned by calling the corresponding
        op in the op_list.

    Examples:
        >>> # xdoctest: +SKIP("no rank")
        >>> send_tensor = torch.arange(2, dtype=torch.float32) + 2 * rank
        >>> recv_tensor = torch.randn(2, dtype=torch.float32)
        >>> send_op = dist.P2POp(dist.isend, send_tensor, (rank + 1) % world_size)
        >>> recv_op = dist.P2POp(
        ...     dist.irecv, recv_tensor, (rank - 1 + world_size) % world_size
        ... )
        >>> reqs = batch_isend_irecv([send_op, recv_op])
        >>> for req in reqs:
        >>>     req.wait()
        >>> recv_tensor
        tensor([2, 3])     # Rank 0
        tensor([0, 1])     # Rank 1

    .. note:: Note that when this API is used with the NCCL PG backend, users must set
        the current GPU device with `torch.cuda.set_device`, otherwise it will
        lead to unexpected hang issues.

        In addition, if this API is the first collective call in the ``group``
        passed to ``dist.P2POp``, all ranks of the ``group`` must participate in
        this API call; otherwise, the behavior is undefined. If this API call is
        not the first collective call in the ``group``, batched P2P operations
        involving only a subset of ranks of the ``group`` are allowed.
    """
    _check_p2p_op_list(p2p_op_list)
    group = p2p_op_list[0].group
    if group is None:
        group = _get_default_group()
    device = p2p_op_list[0].tensor.device

    def peer_kwarg(op: P2POp) -> dict[str, int]:
        key = "group_dst" if op.op is isend else "group_src"
        return {key: op.group_peer}

    if type(group) is ProcessGroup and group._get_backend(device).supports_coalescing:
        # NCCL style coalescing
        with _coalescing_manager(group, device, async_ops=True) as cm:
            for p2p_op in p2p_op_list:
                p2p_op.op(
                    p2p_op.tensor,
                    group=p2p_op.group,
                    tag=p2p_op.tag,
                    **peer_kwarg(p2p_op),
                )

        return cm.works
    else:
        # backend not support coalescing
        reqs = []
        for p2p_op in p2p_op_list:
            work = p2p_op.op(
                p2p_op.tensor,
                group=p2p_op.group,
                tag=p2p_op.tag,
                **peer_kwarg(p2p_op),
            )
            if work:
                reqs.append(work)
        return reqs

