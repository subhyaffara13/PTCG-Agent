
def temperature(device: Device = None) -> int:
    r"""Return the average temperature of the GPU sensor in Degrees C (Centigrades).

    The average temperature is computed based on past sample period as given by `nvidia-smi`.

    Args:
        device (torch.device or int, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    Warning: Each sample period may be between 1 second and 1/6 second,
    depending on the product being queried.
    """
    if not torch.version.hip:
        handle = _get_pynvml_handler(device)
        # 0 refers to the temperature sensor for the GPU die.
        return pynvml.nvmlDeviceGetTemperature(handle, 0)
    else:
        return _get_amdsmi_temperature(device)

