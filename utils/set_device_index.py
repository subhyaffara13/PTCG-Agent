
def set_device_index(device: _device_t, /) -> None:
    r"""Set the current device index to a given device.

    Args:
        device (:class:`torch.device`, str, int): a given device that must match the current
            :ref:`accelerator<accelerators>` device type.

    .. note:: This function is a no-op if this device index is negative.
    """
    device_index = _get_device_index(device, optional=False)
    torch._C._accelerator_setDeviceIndex(device_index)

