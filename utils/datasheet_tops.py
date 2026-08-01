
def datasheet_tops(dtype: torch.dtype, is_tf32: bool = False) -> float | None:
    """
    Get the theoretical TFLOPS of the device for a given dtype. This can throw an exception if the device
    is not in the datasheet list above.
    """
    name: str | None = torch.cuda.get_device_name()
    if name is None:
        log.info("No device found, returning None")
        return None
    device_info = lookup_device_info(name)
    if device_info is None:
        log_str = f"Device {name} not in datasheet, returning None"
        log.info(log_str)
        return None
    if dtype not in device_info.tops:
        log.info(
            "Device %s does not have a datasheet entry for %s, returning None",
            name,
            dtype,
        )
        return None

    return device_info.tops[
        "torch.tf32" if dtype == torch.float32 and is_tf32 else dtype
    ]

