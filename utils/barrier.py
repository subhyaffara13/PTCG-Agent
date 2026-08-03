from typing import Callable

def barrier(
    group: ProcessGroup | None = GroupMember.WORLD,
    async_op: bool = False,
    device_ids=None,
    timeout: timedelta | None = None,
):
    """
    Synchronize all processes.

    This collective blocks processes until the whole group enters this function,
    if async_op is False, or if async work handle is called on wait().

    Args:
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        device_ids ([int], optional): List of device/GPU ids. Only one id is expected.
        timeout (datetime.timedelta, optional): Timeout for barrier.
            If ``None``, the default process group timeout will be used.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    .. note:: `ProcessGroupNCCL` now blocks the cpu thread till the completion of the barrier collective.
    .. note:: `ProcessGroupNCCL` implements barrier as an all_reduce of a 1-element tensor. A device must be chosen
       for allocating this tensor.  The device choice is made by checking in this order (1) the first device passed to
       `device_ids` arg of barrier if not None, (2) the device passed to init_process_group if not None, (3) the device
       that was first used with this process group, if another collective with tensor inputs has been performed, (4)
       the device index indicated by the global rank mod local device count.
    """
    group = group or _get_default_group()

    if _rank_not_in_group(group):
        _warn_not_in_group("barrier")
        return

    opts = BarrierOptions()
    opts.asyncOp = async_op
    if timeout is not None:
        opts.timeout = timeout
    # Detect the accelerator on the machine. If no accelerator is available, it
    # returns CPU.
    device = torch._C._get_accelerator()
    if isinstance(device_ids, list):
        opts.device_ids = device_ids
        # use only the first device id
        opts.device = torch.device(device.type, device_ids[0])
    elif getattr(group, "bound_device_id", None) is not None:
        # Use device id from `init_process_group(device_id=...)`
        opts.device = group.bound_device_id  # type: ignore[assignment]
    elif device.type == "cpu" or _get_object_coll_device(group) == "cpu":
        opts.device = torch.device("cpu")
    else:
        # Use the current device set by the user. If user did not set any, this
        # may use default device 0, causing issues like hang or all processes
        # creating context on device 0.
        opts.device = device
        if group.rank() == 0:
            warnings.warn(  # warn only once
                "barrier(): using the device under current context. "
                "You can specify `device_id` in `init_process_group` to mute this warning.",
                stacklevel=2,
            )

    work = group.barrier(opts=opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def barrier(
    store,
    world_size: int,
    key_prefix: str,
    barrier_timeout: float = 300,
    rank: int | None = None,
    rank_tracing_decoder: Callable[[int], str] | None = None,
    trace_timeout: float = 10,
) -> None:
    """
    A global lock between agents. This will pause all workers until at least
    ``world_size`` workers respond.

    This uses a fast incrementing index to assign waiting ranks and a success
    flag set by the last worker.

    Time complexity: O(1) per worker, O(N) globally.

    Optionally, passing rank will enable tracing of missing ranks on timeouts.
    `rank_tracing_decoder` lambda arg can be used to convert rank data
    into a more meaningful information at an app level (e.g. hostname).

    Note: Since the data is not removed from the store, the barrier can be used
        once per unique ``key_prefix``.
    """

    if rank is None:
        if rank_tracing_decoder is not None:
            raise AssertionError("Tracing requires rank information")

    with store_timeout(store, barrier_timeout):
        last_member_key = _barrier_nonblocking(
            store=store, world_size=world_size, key_prefix=key_prefix
        )
        try:
            store.wait([last_member_key])
        except DistStoreError as e:
            if rank is None:
                raise e
            else:
                missing_ranks = _try_detecting_missing_ranks(
                    store,
                    world_size,
                    key_prefix,
                    rank,
                    rank_tracing_decoder or (lambda x: str(x)),
                    trace_timeout,
                )
                if missing_ranks is not None:
                    raise DistStoreError(
                        "Timed out waiting on barrier on "
                        "rank {}, for key prefix: {} (world_size={}, missing_ranks={}, timeout={})".format(
                            rank,
                            key_prefix,
                            world_size,
                            f"[{', '.join(missing_ranks)}]",
                            barrier_timeout,
                        )
                    ) from None
                else:
                    raise e


def barrier():
    comm = _get_comm()
    if comm is not None:
        comm.Barrier()


def barrier(barrier_id: _ods_ir.Value[_ods_ir.IndexType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> BarrierOp:
  return BarrierOp(barrier_id=barrier_id, loc=loc, ip=ip)


def barrier(*, address_spaces: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, named_barrier: _Optional[_ods_ir.Value] = None, scope: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> BarrierOp:
  return BarrierOp(address_spaces=address_spaces, named_barrier=named_barrier, scope=scope, loc=loc, ip=ip)


def barrier(*, barrier_id: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, number_of_threads: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> BarrierOp:
  return BarrierOp(barrierId=barrier_id, numberOfThreads=number_of_threads, loc=loc, ip=ip)

