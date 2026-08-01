
def _get_pynvml_handler(device: Device = None):
    if not _HAS_PYNVML:
        raise ModuleNotFoundError(
            "nvidia-ml-py does not seem to be installed or it can't be imported."
            # pyrefly: ignore [invalid-inheritance]
        ) from _PYNVML_ERR
    # pyrefly: ignore [import-error, missing-import, missing-module-attribute]
    from pynvml import NVMLError_DriverNotLoaded

    try:
        pynvml.nvmlInit()
    except NVMLError_DriverNotLoaded as e:
        raise RuntimeError("cuda driver can't be loaded, is cuda enabled?") from e

    device = _get_nvml_device_index(device)
    handle = pynvml.nvmlDeviceGetHandleByIndex(device)
    return handle

