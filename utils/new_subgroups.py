
def new_subgroups(
    group_size=None,
    group=None,
    timeout=None,
    backend=None,
    pg_options=None,
    group_desc=None,
):
    """
    Create subgroups of equal size.

    By default, it creates intra-machine subgroups,
    where each of which contains all the ranks of a machine, based on the assumption
    that each machine has the same number of devices.

    This is a convenience API that calls ``new_group`` to generate multiple subgroups.
    It requires that all processes in the main group (i.e. all
    processes that are part of the distributed job) enter this function, even
    if they are not going to be members of the group.

    .. warning::
        If ``group_size`` is passed in, the world size must be divisible by ``group_size``.
        If no ``group_size`` is passed in, it believe that you are creating a group based
        on CUDA and determining the group size by number of CUDA devices, and if not all
        the machines have the same number of devices, the subgroup division will be
        different across nodes and can cause unexpected behaviors. Therefore, if you are
        creating a subgroup that does not depend on CUDA (such as Gloo on CPU), please
        pass in ``group_size`` correctly.

    .. warning::
        See warning `Safe concurrent usage` for `new_group` API for important details about
        using multiple process groups concurrently in a safe manner.

    Args:
        group_size (int, optional): The size of each subgroup. If ``None``,
            the default subgroup size is equal to the number of devices on each machine,
            based on the assumption that each machine has exactly the same
            number of devices. Default is ``None``.
        group (ProcessGroup, optional): The process group to work on. If
            ``None``, the default process group will be used. Default is ``None``.
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
            process group can pick up high priority cuda streams.
        group_desc (str, optional): A string describing the group. Each subgroup will
            inherit its group_desc

    Returns:
        The subgroup containing the current rank, and all the subgroups used for cleanup.

    Examples:
        >>> # Create intra-machine subgroups.
        >>> # xdoctest: +SKIP("need process group init")
        >>> cur_subgroup, subgroups = dist.new_subgroups()
        >>> # Allreduce within the machine.
        >>> rank = dist.get_rank()
        >>> tensor = torch.ones(1, device=rank) * rank
        >>> dist.all_reduce(tensor, group=cur_subgroup)
        >>> tensor
        tensor([28])  # Assume 8 CUDA devices per machine.  28 is sum(range(8)).
        >>> # Cleanup.
        >>> for subgroup in subgroups:
        >>>     dist.destroy_process_group(subgroup)
    """
    if group_size is None:
        if not torch.cuda.is_available():
            raise ValueError(
                "Default group size only takes effect when CUDA is available."
                "If your subgroup using a backend that does not depend on CUDA,"
                "please pass in 'group_size' correctly."
            )
        group_size = torch.cuda.device_count()
    if group_size <= 0:
        raise ValueError(f"The arg 'group_size' ({group_size}) must be positive")

    world_size = get_world_size(group=group)
    if world_size < group_size:
        raise ValueError(
            f"The arg 'group_size' ({group_size}) must not exceed the world size ({world_size})"
        )
    if world_size % group_size != 0:
        raise ValueError(
            f"The world size ({world_size}) must be divisible by '{group_size=}'"
        )

    # TODO: Use itertools.batched(get_process_group_ranks(group=group), group_size) instead when Python 3.12 is supported.
    ranks = get_process_group_ranks(group=group)
    ranks_per_subgroup_list = [
        ranks[i : i + group_size] for i in range(0, len(ranks), group_size)
    ]
    return new_subgroups_by_enumeration(
        ranks_per_subgroup_list,
        timeout=timeout,
        backend=backend,
        pg_options=pg_options,
        group_desc=group_desc,
    )

