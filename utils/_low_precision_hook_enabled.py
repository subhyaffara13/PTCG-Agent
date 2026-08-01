
def _low_precision_hook_enabled(state: _FSDPState) -> bool:
    return state._comm_hook in LOW_PRECISION_HOOKS

