from typing import Any

def _post_backward_reshard(
    state: _FSDPState,
    handle: FlatParamHandle,
    *unused: Any,
) -> None:
    free_unsharded_flat_param = _should_free_in_backward(state, handle)
    _reshard(state, handle, free_unsharded_flat_param)

    # TODO: Post-backward prefetching does not support the multiple handles
    # per module case since the post-backward hook runs per handle, not per
    # group of handles.
    with torch.profiler.record_function(
        "FullyShardedDataParallel._post_backward_prefetch"
    ):
        _prefetch_handle(state, handle, _PrefetchMode.BACKWARD)

