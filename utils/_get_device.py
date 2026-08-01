
def _get_device(device: int | str | torch.device) -> torch.device:
    r"""Return the torch.device type object from the passed in device.

    Args:
        device (torch.device or int): selected device.
    """
    if isinstance(device, str):
        device = torch.device(device)
    elif isinstance(device, int):
        device = torch.device("cuda", device)
    return device


def _get_device(device: int | str | torch.device) -> torch.device:
    r"""Return the torch.device type object from the passed in device.

    Args:
        device (torch.device or int or str): selected device.
    """
    if isinstance(device, str):
        device = torch.device(device)
    elif isinstance(device, int):
        device = torch.device("xpu", device)
    return device


def _get_device(a: ArrayImpl) -> Device:
  devices = a.sharding._internal_device_list
  if len(devices) != 1:
    raise ValueError(
        "When making an array from single-device arrays the input arrays must "
        f"have one shard each. An argument array had {len(devices)} shard(s).")
  return devices[0]

