
def _register_state_dict_hooks_base(
    state: _FSDPState,
    hook_registration_fn_name: str,
    hook: Callable,
    hook_registration_fn_kwargs: dict[str, Any],
) -> None:
    """Registers ``hook`` using ``hook_registration_fn``."""
    if not _is_composable(state):
        getattr(state, hook_registration_fn_name)(hook, **hook_registration_fn_kwargs)
    else:
        handle = state._handle
        if handle:
            getattr(handle._fully_sharded_module, hook_registration_fn_name)(
                hook, **hook_registration_fn_kwargs
            )

