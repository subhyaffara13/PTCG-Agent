
def _get_fqn_to_fsdp_param_info(model: nn.Module) -> dict[str, FSDPParamInfo]:
    """
    Construct the mapping from a param's fqn to its corresponding ``FSDPParamInfo``
    if the param is managed by FSDP. Shared parameters, or original parameters that
    are shared across multiple nn.Modules, are required to belong to one and only
    one FSDP instance and thus correspond to one ``FlatParameter``. Within the one
    ``FlatParameter``, ``FlatParameter._fqns`` only stores the first FQN of a shared
    parameter. Thus, the keys in the mapping are guaranteed to map to unique parameters.
    """

    def module_fn(module, prefix, tree_level, fqn_to_param_info):
        fsdp_state = _get_module_fsdp_state_if_fully_sharded_module(module)
        if fsdp_state is None:
            return
        _lazy_init(fsdp_state, module)
        handle = _module_handle(fsdp_state, module)
        if not handle:
            return
        flat_param = handle.flat_param
        fsdp_param_info = FSDPParamInfo(fsdp_state, handle, {}, [])
        # NOTE: `idx` indexes into the data structures *without* padding
        # elements
        for idx, local_fqn in enumerate(flat_param._fqns):
            fqn = clean_tensor_name(prefix + local_fqn)
            if fqn in fqn_to_param_info:
                if fqn_to_param_info[fqn].handle.flat_param is not flat_param:
                    raise AssertionError(
                        f"Expected fqn_to_param_info[fqn].handle.flat_param is flat_param for {fqn}"
                    )
            fqn_to_param_info[fqn] = fsdp_param_info
            fsdp_param_info.param_indices[fqn] = idx
            if flat_param._params is not None:
                fsdp_param_info.param_requires_grad.append(
                    flat_param._params[idx].requires_grad
                )

    def return_fn(fqn_to_param_info):
        return fqn_to_param_info

    fqn_to_param_info: dict[str, FSDPParamInfo] = {}
    # FlatParameter._fqns stores the local fqn, starting from the root of the
    # FSDP. Using _apply_to_modules() with model (may not be the FSDP root
    # module) allows us to construct the global fqn.
    return _apply_to_modules(
        model,
        module_fn,
        return_fn,
        [fqn for fqn, _ in _named_parameters_with_duplicates(model)],
        fqn_to_param_info,
    )

