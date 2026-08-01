
def _get_compute_device(
    module: nn.Module,
    ignored_params: set[nn.Parameter],
    device_from_device_id: torch.device | None,
    rank: int,
    device_handle: _FSDPDeviceHandle,
) -> torch.device:
    """
    Determine and return this FSDP instance's compute device.

    If the module is already on a non-CPU device, then the compute device is that non-CPU
    device. If the module is on CPU, then the compute device is the current
    device.

    Since this method should be called after materializing the module, any
    non-CPU device should not be meta device. For now, the compute device is
    always a CUDA or CUDA-like device with its explicit index.

    Precondition: ``_check_single_device_module()`` and
    ``_move_module_to_device()``.
    """
    param = next(_get_orig_params(module, ignored_params), None)
    if param is not None and param.device.type != "cpu":
        compute_device = param.device  # Determined by model param placement
    else:
        compute_device = torch.device(device_handle.current_device())
    if device_from_device_id is not None and compute_device != device_from_device_id:
        raise ValueError(
            f"Inconsistent compute device and `device_id` on rank {rank}: "
            f"{compute_device} vs {device_from_device_id}"
        )
    return compute_device

