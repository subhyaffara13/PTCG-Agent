
def sm_is_or_higher_than(device: torch.device, major: int, minor: int) -> bool:
    """
    Returns True if the device's compute capability is (major, minor) or higher.
    Error out if the device is not a CUDA device.
    Returns False if device is a RoCM device.
    Returns True if device is a non-CUDA device.
    """
    if device.type != "cuda":
        return True

    if torch.version.hip is not None:
        # ROCm devices may have different compute capability codes
        return False

    return torch.cuda.get_device_capability(device) >= (major, minor)

