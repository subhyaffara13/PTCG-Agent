
def is_noncontiguous_supported(device):
    return device is None or device.type != "hpu"


def is_noncontiguous_supported(device: torch.device) -> bool:
    return device.type != "hpu"

