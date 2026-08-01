
def _common_pre_state_dict_hook(
    module: nn.Module,
    fsdp_state: _FSDPState,
) -> None:
    """Performs the pre-state_dict tasks shared by all state_dict types."""
    if fsdp_state._device_handle.is_available():
        fsdp_state._device_handle.synchronize()
    # TODO: need to check if this is always correct for composable FSDP.
    _lazy_init(fsdp_state, module)
    if fsdp_state._is_root:
        _reset_flat_param_grad_info_if_needed(fsdp_state._all_handles)

