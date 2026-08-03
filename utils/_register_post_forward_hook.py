import functools

def _register_post_forward_hook(
    state: _FSDPState,
    module: nn.Module,
) -> None:
    """
    Registers a post-forward hook on ``module``. Even if the module has no
    handles, we should register the hook since it will register the module's
    pre-backward hook.
    """
    for forward_handle in state._post_forward_handles:
        forward_handle.remove()
    state._post_forward_handles.clear()
    module_param_handle = state._fully_sharded_module_to_handle.get(module, None)
    hook = functools.partial(
        _post_forward,
        state,
        module_param_handle,
        _post_forward_reshard,
    )
    state._post_forward_handles.append(module.register_forward_hook(hook))

