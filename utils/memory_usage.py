
def memory_usage(device: Device = None) -> int:
    r"""Return the percent of time over the past sample period during which global (device)
    memory was being read or written as given by `nvidia-smi`.

    Args:
        device (torch.device or int, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    Warning: Each sample period may be between 1 second and 1/6 second,
    depending on the product being queried.
    """
    if not torch.version.hip:
        handle = _get_pynvml_handler()
        device = _get_nvml_device_index(device)
        handle = pynvml.nvmlDeviceGetHandleByIndex(device)
        return pynvml.nvmlDeviceGetUtilizationRates(handle).memory
    else:
        return _get_amdsmi_memory_usage(device)

