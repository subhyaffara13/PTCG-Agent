
def _get_device_module(device_type: str):
    device_module = getattr(torch, device_type, None)
    if device_module is None:
        raise RuntimeError(
            f"Device '{device_type}' does not have a corresponding module registered as 'torch.{device_type}'."
        )
    return device_module


def _get_device_module(device="cuda"):
    if device == "meta":
        return torch.device("meta")
    device_module = getattr(torch, device)
    return device_module

