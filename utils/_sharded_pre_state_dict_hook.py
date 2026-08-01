
def _sharded_pre_state_dict_hook(
    fsdp_state: _FSDPState,
    module: nn.Module,
    *args,
    **kwargs,
) -> None:
    """
    Hook that runs before model.state_dict() is called. Check
    ``_full_pre_load_state_dict_hook`` for the detail.
    """
    if (
        _has_fsdp_params(fsdp_state, module)
        and not _module_handle(fsdp_state, module).uses_sharded_strategy
    ):
        raise RuntimeError(
            "``sharded_state_dict`` can only be used when parameters are flatten "
            "and sharded."
        )
    _common_pre_state_dict_hook(module, fsdp_state)
    # Setting offload_to_cpu here does not work even if offload_to_cpu is True.
    # We have to create ShardedTensor first then move it to CPU.
    _common_unshard_pre_state_dict_hook(
        module,
        fsdp_state,
        offload_to_cpu=False,
        rank0_only=False,
    )

