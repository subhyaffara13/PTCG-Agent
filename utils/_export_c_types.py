
def _export_c_types() -> None:
    _public_types_to_change_module = [
        AllreduceCoalescedOptions,
        AllreduceOptions,
        AllToAllOptions,
        BarrierOptions,
        BroadcastOptions,
        GatherOptions,
        PrefixStore,
        ProcessGroup,
        ReduceOp,
        ReduceOptions,
        ReduceScatterOptions,
        ScatterOptions,
        Store,
        DebugLevel,
        get_debug_level,
        Work,
    ]
    for type in _public_types_to_change_module:
        type.__module__ = "torch.distributed.distributed_c10d"

