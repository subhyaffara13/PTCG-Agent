
def _get_fsdp_root_states(module: nn.Module) -> list[_FSDPState]:
    """See :func:`_get_fsdp_root_states_with_modules`."""
    fsdp_root_states, _ = _get_fsdp_root_states_with_modules(module)
    return fsdp_root_states

