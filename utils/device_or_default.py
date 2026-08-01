
def device_or_default(device: DeviceLikeType | None) -> DeviceLikeType:
    return device if device is not None else torch.device("cpu")

