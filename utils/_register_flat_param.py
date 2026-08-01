
def _register_flat_param(state: _FSDPState, module: nn.Module) -> None:
    """
    Registers the flattened parameter to the wrapped module, making it
    visible to ``nn.Module`` methods.

    We do not use :meth:`nn.Module.register_parameter` because we want
    ``FLAT_PARAM`` to always be an attribute but dynamically change whether
    it is visible to ``nn.Module`` methods.
    """
    handle = _module_handle(state, module)
    if _has_fsdp_params(state, module):
        # TODO: figure out the case for the composable APIs.
        cast(nn.Module, module.module)._parameters[FLAT_PARAM] = handle.flat_param

