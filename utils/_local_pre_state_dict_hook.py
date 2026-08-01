
def _local_pre_state_dict_hook(
    fsdp_state: _FSDPState,
    module: nn.Module,
    *args,
    **kwargs,
) -> None:
    """
    Hook that runs before model.state_dict() is called. Right now, pre-state_dict
    hook is not supported by the PyTorch core. So this API is called from
    `_local_post_state_dict_hook()` to simulate the case.
    """
    if (
        _has_fsdp_params(fsdp_state, module)
        and not _module_handle(fsdp_state, module).uses_sharded_strategy
    ):
        raise RuntimeError(
            "``local_state_dict`` can only be used when parameters are flatten "
            "and sharded."
        )
    _common_pre_state_dict_hook(module, fsdp_state)

