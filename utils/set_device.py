
def set_device(device: torch.types.Device) -> None:
    r"""Sets the current device, in CPU we do nothing.

    N.B. This function only exists to facilitate device-agnostic code
    """


def set_device(device: Device) -> None:
    r"""Set the current device.

    Usage of this function is discouraged in favor of :any:`device`. In most
    cases it's better to use ``CUDA_VISIBLE_DEVICES`` environmental variable.

    Args:
        device (torch.device or int): selected device. This function is a no-op
            if this argument is negative.
    """
    device = _get_device_index(device)
    if device >= 0:
        torch._C._cuda_setDevice(device)


def set_device(device: Device) -> None:
    r"""Set the current device.

    Args:
        device (torch.device or int): selected device. This function is a no-op
            if this argument is negative.
    """
    device = _get_device_index(device)
    if device >= 0:
        # pyrefly: ignore [missing-attribute]
        torch._C._mtia_setDevice(device)


def set_device(device):
    """
    Set the default device inside of the wrapped function by decorating it with this function.

    If you would like to use this as a context manager, use device as a
    context manager directly, e.g., ``with torch.device(device)``.
    """
    return lambda func: device_decorator(torch.device(device), func)


def set_device(device: Device) -> None:
    r"""Set the current device.

    Args:
        device (torch.device or int or str): selected device. This function is a
            no-op if this argument is negative.
    """
    _lazy_init()
    device = _get_device_index(device)
    if device >= 0:
        torch._C._xpu_setDevice(device)

