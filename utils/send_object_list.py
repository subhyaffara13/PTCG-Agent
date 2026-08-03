from typing import Any

def send_object_list(
    object_list: list[Any],
    dst: int | None = None,
    group: ProcessGroup | None = None,
    device: torch.device | None = None,
    group_dst: int | None = None,
    use_batch: bool = False,
):
    """
    Sends picklable objects in ``object_list`` synchronously.

    Similar to :func:`send`, but Python objects can be passed in.
    Note that all objects in ``object_list`` must be picklable in order to be
    sent.

    Args:
        object_list (List[Any]): List of input objects to sent.
            Each object must be picklable. Receiver must provide lists of equal sizes.
        dst (int): Destination rank to send ``object_list`` to.
            Destination rank is based on global process group (regardless of ``group`` argument)
        group: (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used. Default is ``None``.
        device (``torch.device``, optional): If not None, the objects are
            serialized and converted to tensors which are moved to the
            ``device`` before sending. Default is ``None``.
        group_dst (int, optional): Destination rank on ``group``.
            Must specify one of ``dst`` and ``group_dst`` but not both
        use_batch (bool, optional): If True, use batch p2p operations instead of
            regular send operations. This avoids initializing 2-rank communicators and
            uses existing entire group communicators. See batch_isend_irecv for usage and
            assumptions. Default is ``False``.
    Returns:
        ``None``.

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
        :func:`send_object_list` uses ``pickle`` module implicitly, which
        is known to be insecure. It is possible to construct malicious pickle
        data which will execute arbitrary code during unpickling. Only call this
        function with data you trust.

    .. warning::
        Calling :func:`send_object_list` with GPU tensors is not well supported
        and inefficient as it incurs GPU -> CPU transfer since tensors would be
        pickled. Please consider using :func:`send` instead.

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
    group_dst = _canonicalize_group_rank(group, dst, group_dst)
    _check_not_self_rank(group, group_dst, "destination")

    if _rank_not_in_group(group):
        _warn_not_in_group("send_object_list")
        return

    # Current device selection.
    # To preserve backwards compatibility, ``device`` is default to ``None``
    # in which case we run current logic of device selection, i.e.
    # ``current_device`` is CUDA if backend is NCCL otherwise CPU device. In the
    # case it is not ``None`` we move the size and object tensors to be
    # sent to this device.
    current_device = device or _get_object_coll_device(group)
    # Serialize object_list elements to tensors on src rank.
    tensor_list, size_list = zip(
        *[_object_to_tensor(obj, current_device, group) for obj in object_list]
    )
    object_sizes_tensor = torch.cat(size_list)

    # Send object sizes
    if use_batch:
        batch_isend_irecv(
            [P2POp(isend, object_sizes_tensor, group_peer=group_dst, group=group)]
        ).pop().wait()
    else:
        send(object_sizes_tensor, group_dst=group_dst, group=group)

    # Concatenate and send serialized object tensors
    # Note: torch.cat will do an extra memory copy to the current device, if the tensor_list
    # has only one element, we can skip the copy.
    if len(tensor_list) == 1:  # type: ignore[possibly-undefined]
        object_tensor = tensor_list[0]
    else:
        object_tensor = torch.cat(tensor_list)

    if use_batch:
        batch_isend_irecv(
            [P2POp(isend, object_tensor, group_peer=group_dst, group=group)]
        ).pop().wait()
    else:
        send(object_tensor, group_dst=group_dst, group=group)

