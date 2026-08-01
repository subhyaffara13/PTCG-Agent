
def is_accelerator_device(device: str | int | torch.device) -> bool:
    """Check if the device is an accelerator. We need to function, as device_map can be "disk" as well, which is not
    a proper `torch.device`.
    """
    if device == "disk":
        return False
    else:
        return torch.device(device).type not in ["meta", "cpu"]

