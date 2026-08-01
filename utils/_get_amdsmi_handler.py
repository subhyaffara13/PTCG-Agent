
def _get_amdsmi_handler(device: Device = None):
    if not _HAS_AMDSMI:
        raise ModuleNotFoundError(
            "amdsmi does not seem to be installed or it can't be imported."
        ) from _AMDSMI_ERR
    try:
        amdsmi.amdsmi_init()
    except amdsmi.AmdSmiException as e:
        raise RuntimeError(
            "amdsmi driver can't be loaded, requires >=ROCm6.0 installation"
        ) from e
    device = _get_amdsmi_device_index(device)
    handle = amdsmi.amdsmi_get_processor_handles()[device]
    return handle

