
def _pre_forward_unshard(
    state: _FSDPState,
    handle: FlatParamHandle | None,
) -> None:
    """Unshards parameters in the pre-forward."""
    if not handle:
        return
    # If the handles have been prefetched, then there is no need to call
    # `_unshard()` again
    if not handle._prefetched:
        _unshard(state, handle, state._unshard_stream, state._pre_unshard_stream)
    handle._needs_pre_forward_unshard = False
    # Don't wait during trace
    if not torch.distributed._functional_collectives.is_torchdynamo_compiling():
        current_stream = state._device_handle.current_stream()
        if state._unshard_event is not None:
            current_stream.wait_event(state._unshard_event)
            state._unshard_event = None
        else:
            current_stream.wait_stream(state._unshard_stream)
    with torch.profiler.record_function(
        "FullyShardedDataParallel._pre_forward_prefetch"
    ):
        _prefetch_handle(state, handle, _PrefetchMode.FORWARD)

