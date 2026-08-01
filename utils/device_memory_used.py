
def device_memory_used(device: Device = None) -> int:
    r"""Return used global (device) memory in bytes as given by `nvidia-smi` or `amd-smi`.

    Args:
        device (torch.device or int, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    """
    if not torch.version.hip:
        handle = _get_pynvml_handler()
        device = _get_nvml_device_index(device)
        handle = pynvml.nvmlDeviceGetHandleByIndex(device)
        return pynvml.nvmlDeviceGetMemoryInfo(handle).used
    else:
        return _get_amdsmi_device_memory_used(device)

