
def get_device(device_map: dict | None, param_name: str, valid_torch_device: bool = False) -> torch.device | str | int:
    """Return the device on which `param_name` should be according to the `device_map`. If `valid_torch_device` is `True`,
    then if the device is `"disk"`, `"cpu"` will be returned instead."""
    device = expand_device_map(device_map, [param_name])[param_name]
    if valid_torch_device and device == "disk":
        return "cpu"
    return device


def get_device(args, kwargs):
    if kwargs.get("device"):
        device = kwargs.get("device")
        if isinstance(device, str):
            device = torch.device(device)
        return device.type

    devices = {arg.device.type for arg in args if isinstance(arg, torch.Tensor)}
    if any(dev == "cuda" for dev in devices):
        return "cuda"
    elif any(dev == "xpu" for dev in devices):
        return "xpu"
    elif any(dev == "hpu" for dev in devices):
        return "hpu"
    elif any(dev == "cpu" for dev in devices):
        return "cpu"
    return None


def get_device(device):
    if device is not None:
        return device
    return torch.empty([]).device  # default device


def get_device(node: Node) -> torch.device:
    return node.meta["val"].device

