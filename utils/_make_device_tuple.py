
def _makeDeviceTuple(device):
    # otTables.Device --> tuple, for making device tables unique
    return _DeviceTuple(
        device.DeltaFormat,
        device.StartSize,
        device.EndSize,
        () if device.DeltaFormat & 0x8000 else tuple(device.DeltaValue),
    )

