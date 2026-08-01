
def _init_ignored_module_states(
    state: _FSDPState,
    module: nn.Module,
    ignored_modules: Iterable[torch.nn.Module] | None,
    ignored_states: Iterable[torch.nn.Parameter]
    | Iterable[torch.nn.Module]
    | None = None,
) -> _FSDPState:
    if ignored_modules is not None and ignored_states is not None:
        raise ValueError(
            "Cannot pass both ignored_modules and ignored_states at the "
            "same time. Please just pass ignored_states."
        )
    ignored_parameters = None
    passed_as_ignored_states = ignored_states is not None
    if passed_as_ignored_states:
        ignored_states_list = list(ignored_states)
        _check_ignored_states(ignored_states_list, True)
    else:
        ignored_states_list = []
        _check_ignored_states(
            list(ignored_modules) if ignored_modules is not None else [], False
        )
    if len(ignored_states_list) > 0:
        if isinstance(ignored_states_list[0], nn.Parameter):
            ignored_parameters = ignored_states_list
        else:
            ignored_modules = ignored_states_list
    state._ignored_modules = _get_ignored_modules(module, ignored_modules)
    state._ignored_params = _get_ignored_params(
        module,
        state._ignored_modules,
        ignored_parameters,
    )
    state._ignored_buffer_names = _get_ignored_buffer_names(
        module,
        state._ignored_modules,
    )
    # TODO: FSDP's contract for buffers is not well-defined. They are
    # implicitly ignored for most functionality since they are not sharded;
    # however, FSDP still imposes some semantics on buffers (e.g. buffer mixed
    # precision). We should formalize this contract and decide if we need to
    # compute and store `_ignored_buffers`.
    return state

