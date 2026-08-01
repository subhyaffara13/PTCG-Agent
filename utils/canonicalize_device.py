
def canonicalize_device(device: DeviceLikeType) -> torch.device:
    if isinstance(device, torch.device):
        return device

    if not isinstance(device, str):
        raise AssertionError(f"device must be torch.device or str, got {type(device)}")
    return torch.device(device)

