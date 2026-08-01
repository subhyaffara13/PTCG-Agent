
def _get_nvml_device_index(device: Device) -> int:
    r"""Return the NVML index of the device, taking CUDA_VISIBLE_DEVICES into account."""
    idx = _get_device_index(device, optional=True)
    visible_devices = _parse_visible_devices()
    if type(visible_devices[0]) is str:
        uuids = _raw_device_uuid_nvml()
        if uuids is None:
            raise RuntimeError("Can't get device UUIDs")
        visible_devices = _transform_uuid_to_ordinals(
            cast(list[str], visible_devices), uuids
        )
    visible_devices = cast(list[int], visible_devices)
    if idx < 0 or idx >= len(visible_devices):
        raise RuntimeError(
            f"device {idx} is not visible (CUDA_VISIBLE_DEVICES={visible_devices})"
        )
    return visible_devices[idx]

