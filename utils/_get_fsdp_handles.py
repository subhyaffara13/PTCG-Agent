
def _get_fsdp_handles(module: nn.Module) -> list:
    """
    Returns all ``FlatParamHandle`` s in the module tree rooted at ``module``
    following the rules in :func:`_get_fsdp_state`.
    """
    handles = [
        fsdp_state._handle
        for fsdp_state in _get_fsdp_states(module)
        if fsdp_state._handle is not None
    ]
    return handles

