
def _raw_device_count_amdsmi() -> int:
    if not _HAS_AMDSMI:
        return -1
    try:
        amdsmi.amdsmi_init()
    except amdsmi.AmdSmiException as e:
        warnings.warn(
            f"Can't initialize amdsmi - Error code: {e.err_code}", stacklevel=2
        )
        return -1
    socket_handles = amdsmi.amdsmi_get_processor_handles()
    return len(socket_handles)

