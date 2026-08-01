
def is_autocast_available(device_type: str) -> bool:
    r"""
    Return a bool indicating if autocast is available on :attr:`device_type`.

    Args:
        device_type(str):  Device type to use. Possible values are: 'cuda', 'cpu', 'mtia', 'maia', 'xpu', and so on.
            The type is the same as the `type` attribute of a :class:`torch.device`.
            Thus, you may obtain the device type of a tensor using `Tensor.device.type`.
    """
    return torch._C._is_autocast_available(device_type)

