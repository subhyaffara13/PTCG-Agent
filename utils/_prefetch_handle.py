
def _prefetch_handle(
    state: _FSDPState,
    current_handle: FlatParamHandle | None,
    prefetch_mode: _PrefetchMode,
) -> None:
    """
    Prefetches the next handles if needed (without synchronization). An empty
    handles key cannot prefetch.
    """
    if not current_handle:
        return
    handle = _get_handle_to_prefetch(state, current_handle)
    if not handle:
        return
    # Temporarily emulate the training state while calling `_unshard` to
    # ensure the correct `as_params` for `_use_unsharded_views()`
    prev_training_state = handle._training_state
    if prefetch_mode == _PrefetchMode.BACKWARD:
        handle._training_state = HandleTrainingState.BACKWARD_PRE
    elif prefetch_mode == _PrefetchMode.FORWARD:
        handle._training_state = HandleTrainingState.FORWARD
    else:
        raise ValueError(f"Invalid prefetch mode on rank {state.rank}: {prefetch_mode}")
    # Prefetch the next set of handles without synchronizing to allow
    # the sync to happen as late as possible to maximize overlap
    _unshard(state, handle, state._unshard_stream, state._pre_unshard_stream)
    handle._training_state = prev_training_state
    handle._prefetched = True

