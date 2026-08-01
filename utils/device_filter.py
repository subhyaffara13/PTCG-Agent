
def device_filter(device: torch.device) -> bool:
    return device.type != "cpu"

