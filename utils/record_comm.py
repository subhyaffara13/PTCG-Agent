
def record_comm(name: str):
    """Context manager to set a custom profiling name for communication collectives.

    When active, all c10d collectives issued within this context will use ``name``
    as their profiling title in the Work base class, overriding the default
    backend-specific name (e.g. ``nccl:all_reduce``). This works across all
    backends without per-backend or per-collective changes.

    Args:
        name (str): The profiling name to associate with collectives.

    Example::
        >>> # xdoctest: +SKIP("undefined vars")
        >>> with dist.record_comm("FSDP::all_gather (layer1)"):
        ...     dist.all_gather_into_tensor(output, input, group=pg)
    """
    prev = torch._C._distributed_c10d._get_comm_profiling_name()
    torch._C._distributed_c10d._set_comm_profiling_name(name)
    try:
        yield
    finally:
        torch._C._distributed_c10d._set_comm_profiling_name(prev)

