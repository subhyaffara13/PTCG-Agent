
def monitored_barrier(
    group: ProcessGroup | None = GroupMember.WORLD,
    timeout=None,
    wait_all_ranks: bool = False,
):
    """
    Synchronize processes similar to ``torch.distributed.barrier``, but consider a configurable timeout.

    It is able to report ranks that did not pass this barrier within the provided timeout.
    Specifically, for non-zero ranks, will block until a send/recv is processed from rank 0.
    Rank 0 will block until all send /recv from other ranks are processed, and will report
    failures for ranks that failed to respond in time. Note that if one rank does not reach the
    monitored_barrier (for example due to a hang), all other ranks would fail in monitored_barrier.

    This collective will block all processes/ranks in the group, until the
    whole group exits the function successfully, making it useful for debugging
    and synchronizing. However, it can have a performance impact and should only
    be used for debugging or scenarios that require full synchronization points
    on the host-side. For debugging purposes, this barrier can be inserted
    before the application's collective calls to check if any ranks are
    desynchronized.

    .. note:: Note that this collective is only supported with the GLOO backend.

    Args:
        group (ProcessGroup, optional): The process group to work on. If
            ``None``, the default process group will be used.
        timeout (datetime.timedelta, optional): Timeout for monitored_barrier.
            If ``None``, the default process group timeout will be used.
        wait_all_ranks (bool, optional): Whether to collect all failed ranks or
            not. By default, this is ``False`` and ``monitored_barrier`` on rank 0
            will throw on the first failed rank it encounters in order to fail
            fast. By setting ``wait_all_ranks=True`` ``monitored_barrier`` will
            collect all failed ranks and throw an error containing information
            about all failed ranks.

    Returns:
        ``None``.

    Example::
        >>> # xdoctest: +SKIP("need process group init")
        >>> # Note: Process group initialization omitted on each rank.
        >>> import torch.distributed as dist
        >>> if dist.get_rank() != 1:
        >>>     dist.monitored_barrier() # Raises exception indicating that
        >>> # rank 1 did not call into monitored_barrier.
        >>> # Example with wait_all_ranks=True
        >>> if dist.get_rank() == 0:
        >>>     dist.monitored_barrier(wait_all_ranks=True) # Raises exception
        >>> # indicating that ranks 1, 2, ... world_size - 1 did not call into
        >>> # monitored_barrier.
    """
    # Need to call rank not in group before using the group, otherwise
    # "Invalid process group" error is raised.
    if _rank_not_in_group(group):
        _warn_not_in_group("monitored_barrier")
        return

    if get_backend(group) != Backend.GLOO:
        raise ValueError("monitored_barrier is only implemented for GLOO backend.")

    if timeout is None:
        timeout = _get_default_timeout(get_backend(group))
    elif isinstance(timeout, float):
        # TODO(whc) apparently some existing test case for monitored_barrier passes in a timeout in float format?
        warnings.warn(
            "Please specify timeout arg as a timedelta. "
            f"Converting current value of {timeout} assuming it represents seconds",
            stacklevel=2,
        )
        timeout = timedelta(seconds=timeout)

    _check_valid_timeout(timeout)

    group_to_use = _get_default_group() if group is None else group
    return group_to_use.monitored_barrier(  # type:ignore[attr-defined]
        timeout, wait_all_ranks=wait_all_ranks
    )

