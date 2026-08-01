
def _device_capability(group: ProcessGroup | None = None) -> list[str]:
    """
    Return the device type(s) supported by ``group``.

    Args:
        group (ProcessGroup, optional): The process group to query. If None,
            the default process group will be used.

    Returns:
        List[str]: A list of device types supported by ``group``.
    """
    group = group or _get_default_group()
    return [device.type for device in group._device_types]

