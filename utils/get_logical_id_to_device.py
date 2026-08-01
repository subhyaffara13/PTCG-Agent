
def get_logical_id_to_device(devices: list[Device]) -> dict[int, Device]:
    """Get a mapping from device logical ID to Device object."""
    logical_id_to_device: dict[int, Device] = {}
    for d in devices:
        logical_id_to_device[d.logical_id] = d
    return logical_id_to_device

