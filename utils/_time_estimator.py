
def _time_estimator(
    group: ProcessGroup | None = None,
    device: torch.device | None = None,
):
    """
    Context manager used to estimate time of collectives.
    Within the context manager, nothing is actually run and the backend just simulates
    the collective time only.

    Args:
        group (`ProcessGroup`, optional): The process group to work on. If None,
            the default process group will be used.
        device (`torch.device`, optional): Default is None, set to a device if
            there isn't a `**_coalesced` implementation by the backend.

    Examples:
        >>> # xdoctest: +SKIP("no rank")
        >>> # Synchronous ops
        >>> with _time_estimator() as cm:
        >>>     for i in range(num_colls):
        >>>         dist.all_reduce(tensors[i])
        >>> # estimate time is stored in cm.estimated_time

    .. warning::
       :func:`_time_estimator` currently only support NCCL backend but it can
       easily be extended to other backends.

       Also a NCCL communicator needs to be created because only with a real communicator can we do accurate estimation.
       The communicator internally has knowledge about the links it runs on
       (e.g. intra-node or inter-node, whether the links are NVLink or PCI-e or IB).
    """
    # TODO: We need to also support torch inductor for the time estimator.
    group = group or _get_default_group()
    device = device or _get_pg_default_device(group)
    backend = group._get_backend(device)
    if not backend.supports_time_estimate:
        raise NotImplementedError(
            f"collective time estimator is not supported in the current version of backend {backend}"
        )
    backend._start_time_estimate()  # type: ignore[attr-defined]
    cm = _TimeEstimator()
    yield cm
    cm.estimated_time = backend._end_time_estimate()  # type: ignore[attr-defined]

