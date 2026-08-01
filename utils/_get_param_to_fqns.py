
def _get_param_to_fqns(
    model: torch.nn.Module,
    dedup_shared_params: bool = True,
) -> dict[nn.Parameter, list[str]]:
    """
    Constructs a mapping from parameter to a list of its \"canonical\" FQNs. Here,
    we use canonical to mean the fully-qualified name assigned to the parameter
    based on its position in the original nn.Module hierarchy before any wrapper
    or parallelism has been applied to it. This is in contrast to FQNs that may be
    generated after parallelisms or wrappers have been applied to the model.

    Each normal parameter maps to a singleton list containing its FQN, while each
    ``FlatParameter`` maps to a list of its original parameter FQNs, which may
    have length greater than one.  All FQNs are prefixed starting from ``model``.

    In the case where FSDP was applied with ``use_orig_params=True``, there should be no
    ``FlatParameter`` s registered to the model's modules and this mapping will only
    contain mappings from ``nn.Parameter`` s to singleton FQN lists.

    It is only in the case where FSDP was applied with ``use_orig_params=False`` where
    a ``FlatParameter`` will be registered in place of the original parameters and there
    will be mappings from each ``FlatParameter`` to lists of FQNs corresponding to the
    original parameters.

    Args:
        model (torch.nn.Module): Root module (which may or may not be a
            :class:`FullyShardedDataParallel` instance).
        dedup_shared_params (bool): For shared parameters, if ``True``, only
            includes the FQNs corresponding to the first encounter of the
            shared parameter in the module traversal; if ``False``, then
            includes the FQNs across all encounters. (Default: ``True``)
    """

    def module_fn(module, prefix, tree_level, param_to_fqns):
        for param_name, param in _named_parameters_with_duplicates(
            module, recurse=False
        ):
            local_fqns = (
                param._fqns
                if isinstance(param, flat_param_file.FlatParameter)
                else [param_name]
            )  # prefixed from `module`
            global_fqns = [
                clean_tensor_name(prefix + name) for name in local_fqns
            ]  # prefixed from the top level `model` (i.e. including `prefix`)
            is_shared_param = param in param_to_fqns
            if not is_shared_param:
                param_to_fqns[param] = global_fqns
            else:
                if isinstance(param, flat_param_file.FlatParameter):
                    # DMP overwrites `named_parameters` and skip (advance to
                    # the next child module) the wrapped_module (e.g.,
                    # _dmp_wrapped_module and _fsdp_wrapped_module). When a user
                    # calls `named_child` to traverse the module recursively and
                    # calls `named_parameters` with `recurse=False`, parameters
                    # will be traversed more than once.
                    # This hack is specified designed for DMP + FSDP. We
                    # overwrite the flat_parameters traversal result to only obtain
                    # the last one, which happens to be the correct one.
                    #
                    # TODO: Remove this hack once DMP + FSDP is not supported.
                    warnings.warn(
                        "FlatParameter is being traversed more than once. "
                        "This case should only happen when using "
                        "DistributedModelParallel with FullyShardedDataParallel.",
                        stacklevel=2,
                    )
                    param_to_fqns[param] = global_fqns
                elif not dedup_shared_params:
                    param_to_fqns[param].extend(global_fqns)

    def return_fn(param_to_fqns):
        return param_to_fqns

    param_to_unflat_param_names: dict[torch.nn.Parameter, list[str]] = {}
    return _apply_to_modules(
        model,
        module_fn,
        return_fn,
        [key for key, _ in _named_parameters_with_duplicates(model)],
        param_to_unflat_param_names,
    )

