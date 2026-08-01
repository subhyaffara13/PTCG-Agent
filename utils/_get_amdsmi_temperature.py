
def _get_amdsmi_temperature(device: Device = None) -> int:
    handle = _get_amdsmi_handler(device)
    return amdsmi.amdsmi_get_temp_metric(
        handle,
        amdsmi.AmdSmiTemperatureType.JUNCTION,
        amdsmi.AmdSmiTemperatureMetric.CURRENT,
    )

