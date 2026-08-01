
def _has_fsdp_params(state: _FSDPState, module: nn.Module) -> bool:
    """Returns if ``module`` has parameters managed by FSDP."""
    return _module_handle(state, module) is not None

