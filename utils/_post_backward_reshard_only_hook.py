
def _post_backward_reshard_only_hook(
    state: _FSDPState,
    handle: FlatParamHandle,
    *unused: Any,
) -> None:
    with torch.profiler.record_function(
        "FullyShardedDataParallel._post_backward_hook_reshard_only"
    ):
        # `_pre_backward_hook` may not get executed
        # if forward output does not require grad
        # overwrite IDLE state for post-backward prefetching
        state.training_state = TrainingState.FORWARD_BACKWARD
        handle._training_state = HandleTrainingState.BACKWARD_POST
        _post_backward_reshard(state, handle)

