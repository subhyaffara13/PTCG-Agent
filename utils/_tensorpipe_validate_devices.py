
def _tensorpipe_validate_devices(devices, device_count):
    return all(
        d.type == "cpu" or (d.type == "cuda" and 0 <= d.index < device_count)
        for d in devices
    )

