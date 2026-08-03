import uuid

def _raw_device_uuid_amdsmi() -> list[str] | None:
    from ctypes import byref, c_int, c_void_p, CDLL, create_string_buffer

    if not _HAS_AMDSMI:
        return None
    try:
        amdsmi.amdsmi_init()
    except amdsmi.AmdSmiException:
        warnings.warn("Can't initialize amdsmi", stacklevel=2)
        return None
    try:
        socket_handles = amdsmi.amdsmi_get_processor_handles()
        dev_count = len(socket_handles)
    except amdsmi.AmdSmiException:
        warnings.warn("Can't get amdsmi device count", stacklevel=2)
        return None
    uuids: list[str] = []
    for idx in range(dev_count):
        try:
            handler = amdsmi.amdsmi_get_processor_handles()[idx]
        except amdsmi.AmdSmiException:
            warnings.warn("Cannot get amd device handler", stacklevel=2)
            return None
        try:
            uuid = amdsmi.amdsmi_get_gpu_asic_info(handler)["asic_serial"][
                2:
            ]  # Removes 0x prefix from serial
        except amdsmi.AmdSmiException:
            warnings.warn("Cannot get uuid for amd device", stacklevel=2)
            return None
        uuids.append(
            str(uuid).lower()
        )  # Lower-case to match expected HIP_VISIBLE_DEVICES uuid input
    return uuids

