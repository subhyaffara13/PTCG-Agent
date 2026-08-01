
def memory_stats_as_nested_dict(device: "Device" = None) -> dict[str, Any]:
    r"""Return the result of :func:`~torch.cuda.memory_stats` as a nested dictionary."""
    if not is_initialized():
        return {}
    device = _get_device_index(device, optional=True)
    return torch._C._cuda_memoryStats(device)


def memory_stats_as_nested_dict(device: Device = None) -> dict[str, Any]:
    r"""Return the result of :func:`~torch.xpu.memory_stats` as a nested dictionary."""
    if not is_initialized():
        return {}
    device = _get_device_index(device, optional=True)
    return torch._C._xpu_memoryStats(device)

