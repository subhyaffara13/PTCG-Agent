
def _init_runtime_state(
    state: _FSDPState,
) -> _FSDPState:
    _root_pre_forward_handles: list[RemovableHandle] = []
    state._root_pre_forward_handles = _root_pre_forward_handles
    _pre_forward_handles: list[RemovableHandle] = []
    state._pre_forward_handles = _pre_forward_handles
    _post_forward_handles: list[RemovableHandle] = []
    state._post_forward_handles = _post_forward_handles
    state._sync_gradients = True
    state._comm_hook = None
    state._comm_hook_state = None
    # Used to prevent running the pre-backward hook multiple times
    return state

