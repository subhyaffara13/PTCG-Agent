
def _normalization_device(
    custom_backend_name: str, device: int | str | torch.device | None = None
) -> int:
    def _get_current_device_index():
        _get_device_index = "current_device"
        if hasattr(torch, custom_backend_name) and hasattr(
            getattr(torch, custom_backend_name), _get_device_index
        ):
            return getattr(getattr(torch, custom_backend_name), _get_device_index)()
        else:
            # The default device index is 0.
            return 0

    if device is None:
        return _get_current_device_index()
    # if isinstance(device, str), this means that the parameter passed in is in the string format "foo:0"
    # convert str object to torch.device object, and then process it uniformly
    elif isinstance(device, str):
        device = torch.device(device)

    # variable device can only be torch.device type or int type
    if isinstance(device, torch.device):
        if device.type != custom_backend_name:
            raise RuntimeError(f"Invalid device, must be {custom_backend_name} device")
        elif device.index is None:
            device_idx = _get_current_device_index()
        else:
            device_idx = device.index
    # if isinstance(device, int), we can take the index number directly
    else:
        device_idx = device
    return device_idx

