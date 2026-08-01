
def _check_module_states_for_sync_module_states(
    module_states: list[torch.Tensor],
) -> None:
    if module_states and any(
        tensor.device == torch.device("cpu") for tensor in module_states
    ):
        raise ValueError(
            "The module has CPU parameters or buffers when `sync_module_states=True`, "
            "which requires them to be on GPU. Please specify the `device_id` argument "
            "or move the module to GPU before passing it to FSDP."
        )

