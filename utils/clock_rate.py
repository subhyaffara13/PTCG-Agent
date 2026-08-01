
def clock_rate(device: Device = None) -> int:
    r"""Return the clock speed of the GPU SM in MHz (megahertz) over the past sample period as given by `nvidia-smi`.

    Args:
        device (torch.device or int, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    Warning: Each sample period may be between 1 second and 1/6 second,
    depending on the product being queried.
    """
    if not torch.version.hip:
        handle = _get_pynvml_handler(device)
        return pynvml.nvmlDeviceGetClockInfo(handle, 1)
    else:
        return _get_amdsmi_clock_rate(device)

