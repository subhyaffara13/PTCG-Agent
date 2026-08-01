
def _to_device_list(devices: list[DeviceType]) -> list[torch.device]:
    return list(map(_to_device, devices))

