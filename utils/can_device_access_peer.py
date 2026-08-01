
def can_device_access_peer(device: Device, peer_device: Device) -> bool:
    r"""Check if peer access between two devices is possible."""
    _lazy_init()
    device = _get_device_index(device, optional=True)
    peer_device = _get_device_index(peer_device)
    if device < 0 or device >= device_count():
        raise AssertionError("Invalid device id")
    if peer_device < 0 or peer_device >= device_count():
        raise AssertionError("Invalid peer device id")
    return torch._C._cuda_canDeviceAccessPeer(device, peer_device)


def can_device_access_peer(device: Device, peer: Device) -> bool:
    r"""Query whether a device can access a peer device's memory.

    Args:
        device (torch.device or int or str): selected device.
        peer (torch.device or int or str): peer device to query access to.

    Returns:
        bool: ``True`` if ``device`` can access ``peer``, ``False`` otherwise.
    """
    _lazy_init()
    device = _get_device_index(device, optional=True)
    peer = _get_device_index(peer, optional=True)
    return torch._C._xpu_canDeviceAccessPeer(device, peer)

