
def _get_amdsmi_device_index(device: Device) -> int:
    r"""Return the amdsmi index of the device, taking visible_devices into account."""
    idx = _get_device_index(device, optional=True)
    visible_devices = _parse_visible_devices()
    visible_device_is_str = type(visible_devices[0]) is str
    if visible_device_is_str:
        uuids = _raw_device_uuid_amdsmi()
        if uuids is None:
            raise RuntimeError("Can't get device UUIDs")
        visible_devices_str = cast(
            list[str], visible_devices
        )  # Create str variable for mypy
        visible_devices = _transform_uuid_to_ordinals(visible_devices_str, uuids)
    idx_map = dict(enumerate(cast(list[int], visible_devices)))
    if idx not in idx_map:
        raise RuntimeError(
            f"device {idx} is not visible (HIP_VISIBLE_DEVICES={visible_devices})"
        )
    if visible_device_is_str:
        return idx_map[idx]
    else:
        return _get_amdsmi_device_index_from_hip_index(idx_map[idx])

