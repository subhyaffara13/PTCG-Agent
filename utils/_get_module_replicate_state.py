
def _get_module_replicate_state(module: nn.Module) -> _ReplicateState | None:
    state = _get_module_state(module)
    if isinstance(state, _ReplicateState):
        return state
    return None

