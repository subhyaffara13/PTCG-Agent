
def _device_has_foreach_support(device: torch.device) -> bool:
    return (
        device.type in (_get_foreach_kernels_supported_devices() + ["cpu"])
        and not torch.jit.is_scripting()
    )

