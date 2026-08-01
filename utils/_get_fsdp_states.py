
def _get_fsdp_states(module: nn.Module) -> list[_FSDPState]:
    """See :func:`_get_fsdp_states_with_modules`."""
    fsdp_states, _ = _get_fsdp_states_with_modules(module)
    return fsdp_states

