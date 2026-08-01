
def get_vendor_id_for_device_type(device_type: str) -> OrtDeviceVendorId | None:
    if device_type == "cuda":
        return OrtDeviceVendorId.NVIDIA
    elif device_type == "dml":
        return OrtDeviceVendorId.MICROSOFT
    elif device_type == "cann":
        return OrtDeviceVendorId.HUAWEI
    else:
        return None

