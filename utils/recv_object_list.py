from typing import Any

def recv_object_list(
    object_list: list[Any],
    src: int | None = None,
    group: ProcessGroup | None = None,
    device: torch.device | None = None,
    group_src: int | None = None,
    use_batch: bool = False,
):
    """
    Receives picklable objects in ``object_list`` synchronously.

    Similar to :func:`recv`, but can receive Python objects.

    Args:
        object_list (List[Any]): List of objects to receive into.
            Must provide a list of sizes equal to the size of the list being sent.
        src (int, optional): Source rank from which to recv ``object_list``.
            Source rank is based on global process group (regardless of ``group`` argument)
            Will receive from any rank if set to None. Default is ``None``.
        group: (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used. Default is ``None``.
        device (``torch.device``, optional): If not None, receives on this device.
            Default is ``None``.
        group_src (int, optional): Destination rank on ``group``.  Invalid to specify both ``src`` and ``group_src``.
        use_batch (bool, optional): If True, use batch p2p operations instead of
            regular send operations. This avoids initializing 2-rank communicators and
            uses existing entire group communicators. See batch_isend_irecv for usage and
            assumptions. Default is ``False``.

    Returns:
        Sender rank. -1 if rank is not part of the group. If rank is part of the group,
        ``object_list`` will contain the sent objects from ``src`` rank.

    .. note:: For NCCL-based process groups, internal tensor representations
        of objects must be moved to the GPU device before communication takes
        place. In this case, the device used is given by
        ``torch.cuda.current_device()`` and it is the user's responsibility to
        ensure that this is set so that each rank has an individual GPU, via
        ``torch.cuda.set_device()``.

    .. warning::
        Object collectives have a number of serious performance and scalability
        limitations.  See :ref:`object_collectives` for details.

    .. warning::
        :func:`recv_object_list` uses ``pickle`` module implicitly, which
        is known to be insecure. It is possible to construct malicious pickle
        data which will execute arbitrary code during unpickling. Only call this
        function with data you trust.

    .. warning::
        Calling :func:`recv_object_list` with GPU tensors is not well supported
        and inefficient as it incurs GPU -> CPU transfer since tensors would be
        pickled. Please consider using :func:`recv` instead.

    Example::
        >>> # xdoctest: +SKIP("need process group init")
        >>> # Note: Process group initialization omitted on each rank.
        >>> import torch.distributed as dist
        >>> # Assumes backend is not NCCL
        >>> device = torch.device("cpu")
        >>> if dist.get_rank() == 0:
        >>>     # Assumes world_size of 2.
        >>>     objects = ["foo", 12, {1: 2}] # any picklable object
        >>>     dist.send_object_list(objects, dst=1, device=device)
        >>> else:
        >>>     objects = [None, None, None]
        >>>     dist.recv_object_list(objects, src=0, device=device)
        >>> objects
        ['foo', 12, {1: 2}]
    """
    group = _group_or_default_group(group)
    group_src = _canonicalize_group_rank(group, src, group_src)
    _check_not_self_rank(group, group_src, "source")

    if _rank_not_in_group(group):
        _warn_not_in_group("recv_object_list")
        return -1

    # Current device selection.
    # To preserve backwards compatibility, ``device`` is default to ``None``
    # in which case we run current logic of device selection, i.e.
    # ``current_device`` is CUDA if backend is NCCL otherwise CPU device. In the
    # case it is not ``None`` we move the size and object tensors to be
    # received to this device.
    current_device = device or _get_object_coll_device(group)
    object_sizes_tensor = torch.empty(
        len(object_list), dtype=torch.long, device=current_device
    )

    # Receive object sizes
    if use_batch:
        work = batch_isend_irecv(
            [
                P2POp(
                    irecv,
                    object_sizes_tensor,
                    group_peer=group_src,
                    group=group,
                )
            ]
        ).pop()
        work.wait()
        rank_sizes = get_global_rank(group, group_src)
    else:
        rank_sizes = recv(object_sizes_tensor, group=group, group_src=group_src)

    # Tensor to receive serialized objects into.
    object_tensor = torch.empty(  # type: ignore[call-overload]
        torch.sum(object_sizes_tensor).item(),  # type: ignore[arg-type]
        dtype=torch.uint8,
        device=current_device,
    )

    if use_batch:
        work = batch_isend_irecv(
            [
                P2POp(
                    irecv,
                    object_tensor,
                    group_peer=group_src,
                    group=group,
                )
            ]
        ).pop()
        work.wait()
        rank_objects = get_global_rank(group, group_src)
    else:
        rank_objects = recv(object_tensor, group=group, group_src=group_src)
    if rank_sizes != rank_objects:
        raise AssertionError("Mismatch in return ranks for object sizes and objects.")
    # Deserialize objects using their stored sizes.
    offset = 0
    for i, obj_size in enumerate(object_sizes_tensor):
        obj_view = object_tensor[offset : offset + obj_size]
        obj_view = obj_view.type(torch.uint8)
        offset += obj_size
        object_list[i] = _tensor_to_object(obj_view, obj_size, group)
    return rank_objects

