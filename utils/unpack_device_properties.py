
def unpack_device_properties(
    properties: PackedDeviceProperties | None = None,
) -> DeviceProperties:
    """
    Unpack a `PackedDeviceProperties` tuple into consistently formatted `DeviceProperties` tuple. If properties is None, it is fetched.
    """
    if properties is None:
        return get_device_properties()
    device_type, major_minor = properties
    if major_minor is None:
        major, minor = None, None
    elif isinstance(major_minor, int):
        major, minor = major_minor, None
    else:
        major, minor = major_minor
    return device_type, major, minor

