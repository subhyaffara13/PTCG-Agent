
def _full_pre_state_dict_hook(
    fsdp_state: _FSDPState,
    module: nn.Module,
    *args,
    **kwargs,
) -> None:
    """
    Hook that runs before model.state_dict() is called. pre-state_dict hook is
    not actually supported by ``nn.Module``. As a result, this API is called
    from ``_full_post_state_dict_hook()`` to simulate the case. Once pre-state_dict
    is supported in ``nn.Module``, this hook will be registered as a hook in
    ``nn.Module``.
    """
    if getattr(fsdp_state, "_device_mesh", False):
        fsdp_state._device_mesh._get_root_mesh()

    _common_pre_state_dict_hook(module, fsdp_state)
    _common_unshard_pre_state_dict_hook(
        module,
        fsdp_state,
        offload_to_cpu=fsdp_state._state_dict_config.offload_to_cpu,
        rank0_only=cast(FullStateDictConfig, fsdp_state._state_dict_config).rank0_only,
    )

