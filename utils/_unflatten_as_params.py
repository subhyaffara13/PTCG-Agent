
def _unflatten_as_params(state: _FSDPState, module: nn.Module) -> Generator:
    """
    Assumes that the flattened parameter is unsharded. When in the context,
    de-registers the flattened parameter and unflattens the original
    parameters as ``nn.Parameter`` views into the flattened parameter.
    After the context, re-registers the flattened parameter and restores
    the original parameters as ``Tensor`` views into the flattened
    parameter.
    """
    handle = _module_handle(state, module)
    if not handle:
        yield
    else:
        _deregister_flat_param(state, module)
        try:
            with handle.unflatten_as_params():
                yield
        finally:
            if not handle._use_orig_params:
                _register_flat_param(state, module)

