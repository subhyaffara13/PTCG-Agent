
def _unshard_params(
    module: nn.Module,
    recurse: bool,
    writeback: bool,
    rank0_only: bool,
    offload_to_cpu: bool,
    with_grads: bool,
):
    """
    This unshards FSDP-managed parameters for all modules with FSDP applied in
    the module tree rooted at ``module``.
    """
    if not recurse:
        optional_state = _get_module_fsdp_state(module)
        if optional_state is None:
            with contextlib.nullcontext():
                yield
            return
        states_and_modules = ([optional_state], [module])
    else:
        states_and_modules = traversal_utils._get_fsdp_states_with_modules(module)
    with contextlib.ExitStack() as stack:
        for state, module in zip(*states_and_modules):
            stack.enter_context(
                _unshard_params_for_summon(
                    module=module,
                    state=state,
                    writeback=writeback,
                    rank0_only=rank0_only,
                    offload_to_cpu=offload_to_cpu,
                    with_grads=with_grads,
                )
            )
        yield

