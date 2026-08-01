
def _get_fsdp_root_states_with_modules(
    module: nn.Module,
) -> tuple[list[_FSDPState], list[nn.Module]]:
    """
    Returns a tuple containing:
    1. A list of the root ``_FSDPState`` instances in the module tree rooted at
    ``module`` without any duplicates and following the ``module.modules()``
    traversal order (which is assumed to be depth-first).
    2. A corresponding list of the root modules owning the states in the first
    list.

    This is similar to :func:`_get_fsdp_states_with_modules` except that we
    must call :func:`_is_fsdp_root` to force a lazy initialization to determine
    the FSDP root in case lazy initialization has not yet happened.
    """
    fsdp_root_states: list[_FSDPState] = []
    fsdp_root_modules: list[nn.Module] = []
    visited_fsdp_states: set[_FSDPState] = set()
    # NOTE: This function assumes that `module.modules()` proceeds top-down.
    for submodule in module.modules():
        optional_state = _get_module_fsdp_state(submodule)
        if (
            optional_state is not None
            and optional_state not in visited_fsdp_states
            and _is_fsdp_root(optional_state, submodule)
        ):
            visited_fsdp_states.add(optional_state)
            fsdp_root_states.append(optional_state)
            fsdp_root_modules.append(submodule)
    return fsdp_root_states, fsdp_root_modules

