from typing import Optional

def _module_handle(state: _FSDPState, module: nn.Module) -> Optional["FlatParamHandle"]:
    """
    Returns the ``FlatParamHandle`` s corresponding to ``module``. This is
    the handle that contains some parameter in ``module``.
    """
    if _is_composable(state):
        # A valid FSDP state may have no managed parameters and hence no
        # handles, meaning no entry in `_fully_sharded_module_to_handles`
        if state._handle is None:
            return None
        if module not in state._fully_sharded_module_to_handle:
            raise AssertionError(
                f"Expects a fully sharded module but got {module} on rank {state.rank}"
            )
        return state._fully_sharded_module_to_handle[module]
    else:
        # NOTE: This assumes `module` is a `FullyShardedDataParallel` instance.
        return module._handle

