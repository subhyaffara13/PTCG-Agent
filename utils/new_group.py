
def new_group(
    ranks=None,
    timeout=None,
    backend=None,
    pg_options=None,
    use_local_synchronization: bool = False,
    group_desc=None,
    device_id: torch.device | None = None,
    sort_ranks: bool = True,
):
    """
    Create a new distributed group.

    This function requires that all processes in the main group (i.e. all
    processes that are part of the distributed job) enter this function, even
    if they are not going to be members of the group. Additionally, groups
    should be created in the same order in all processes.

    .. warning::
        Safe concurrent usage:
        When using multiple process groups with the ``NCCL`` backend, the user
        must ensure a globally consistent execution order of collectives across
        ranks.

        If multiple threads within a process issue collectives, explicit
        synchronization is necessary to ensure consistent ordering.

        When using async variants of torch.distributed communication APIs,
        a work object is returned and the communication kernel is
        enqueued on a separate CUDA stream, allowing overlap of communication
        and computation. Once one or more async ops have been issued on one process
        group, they must be synchronized with other cuda streams by calling `work.wait()`
        before using another process group.

        See `Using multiple NCCL communicators concurrently
        <https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently>`
        for more details.

    Args:
        ranks (list[int]): List of ranks of group members. If ``None``, will be
            set to all ranks. Default is ``None``.
        timeout (timedelta, optional): see `init_process_group` for details and default value.
        backend (str or Backend, optional): The backend to use. Depending on
            build-time configurations, valid values are ``gloo`` and ``nccl``.
            By default uses the same backend as the global group. This field
            should be given as a lowercase string (e.g., ``"gloo"``), which can
            also be accessed via :class:`Backend` attributes (e.g.,
            ``Backend.GLOO``). If ``None`` is passed in, the backend
            corresponding to the default process group will be used. Default is
            ``None``.
        pg_options (ProcessGroupOptions, optional): process group options
            specifying what additional options need to be passed in during
            the construction of specific process groups. i.e. for the ``nccl``
            backend, ``is_high_priority_stream`` can be specified so that
            process group can pick up high priority cuda streams. For other available options to config nccl,
            See https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/api/types.html#ncclconfig-tuse_local_synchronization
            (bool, optional): perform a group-local barrier at the end of the process group creation.
            This is different in that non-member ranks don't need to call into API and don't
            join the barrier.
        group_desc (str, optional): a string to describe the process group.
        device_id (torch.device, optional): a single, specific device
            to "bind" this process to,  The `new_group` call will try to initialize
            a communication backend immediately for the device if this field is given.
        sort_ranks (bool, optional): If ``True`` (the default), sort the
            ``ranks`` list before creating the group. If ``False``, preserve
            the caller-provided rank order so that position in the ``ranks``
            list determines group rank.  All processes must pass the identical
            ``ranks`` list.  Default is ``True``.

    Returns:
        A handle of distributed group that can be given to collective calls or
        GroupMember.NON_GROUP_MEMBER if the rank is not part of ``ranks``.

    N.B. use_local_synchronization doesn't work with MPI.

    N.B. While use_local_synchronization=True can be significantly faster with larger
    clusters and small process groups, care must be taken since it changes cluster behavior
    as non-member ranks don't join the group barrier().

    N.B. use_local_synchronization=True can lead to deadlocks when each rank creates
    multiple overlapping process groups. To avoid that, make sure all ranks follow the
    same global creation order.
    """
    return _new_group_with_tag(
        ranks,
        timeout,
        backend,
        pg_options,
        None,
        use_local_synchronization=use_local_synchronization,
        group_desc=group_desc,
        device_id=device_id,
        sort_ranks=sort_ranks,
    )


def new_group(
    backend: str,
    timeout: timedelta,
    device: str | torch.device,
    **kwargs: object,
) -> ProcessGroup:
    """
    Create a new process group with the given backend and options. This group is
    independent and will not be globally registered and thus not usable via the
    standard torch.distributed.* APIs.

    Args:
        backend: The backend to use for the process group.
        timeout: The timeout for collective operations.
        device: The device to use for the process group.
        **kwargs: All remaining arguments are passed to the backend constructor.
                  See the backend specific documentation for details.

    Returns:
        A new process group.
    """
    if backend not in _BACKENDS:
        raise ValueError(f"Backend {backend} not registered")

    device = torch.device(device)

    store, rank, world_size = next(iter(rendezvous("env://")))
    store.set_timeout(timeout)

    return _BACKENDS[backend](store, rank, world_size, timeout, device, **kwargs)

