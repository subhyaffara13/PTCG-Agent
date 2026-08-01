
def get_xpu_codename() -> XPUCodename | None:
    device_id = torch.xpu.get_device_capability()["device_id"]
    return _DEVICE_ID_TO_CODENAME.get(device_id)

