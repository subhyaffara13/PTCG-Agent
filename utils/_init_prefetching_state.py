
def _init_prefetching_state(
    state: _FSDPState,
    backward_prefetch: BackwardPrefetch,
    forward_prefetch: bool,
) -> _FSDPState:
    state.backward_prefetch = backward_prefetch
    state.forward_prefetch = forward_prefetch
    # The data structures use tuples of handles to generalize over the case
    # where a module's forward involves multiple handles.
    return state

