
def _get_module_fsdp_state(module: nn.Module) -> _FSDPState | None:
    state = _get_module_state(module)
    if state is None or not isinstance(state, _FSDPState):
        return None
    return state


def _get_module_fsdp_state(module: nn.Module) -> FSDPState | None:
    state = _get_module_state(module)
    if isinstance(state, FSDPState):
        return state
    return None

