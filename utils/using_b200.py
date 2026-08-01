
def using_b200() -> bool:
    """Returns true if the device is a NVIDIA B200, otherwise returns false."""
    if not torch.cuda.is_available():
        return False
    # compute capability 10.0 or 10.0a is NVIDIA B200
    device_properties = torch.cuda.get_device_properties(torch.cuda.current_device())
    return device_properties.major == 10

