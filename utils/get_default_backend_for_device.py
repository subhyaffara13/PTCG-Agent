
def get_default_backend_for_device(device: str | torch.device) -> str:
    """
    Return the default backend for the given device.

    Args:
        device (Union[str, torch.device]): The device to get the default backend for.

    Returns:
        The default backend for the given device as a lower case string.

    """
    if isinstance(device, torch.device):
        device_str = device.type
    else:
        device_str = torch.device(device).type

    backend = Backend.default_device_backend_map.get(device_str)
    if backend is None:
        raise ValueError(f"Default backend not registered for device : {device}")

    return backend

