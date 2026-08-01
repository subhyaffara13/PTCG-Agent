
def onlyPRIVATEUSE1(fn):
    device_type = torch._C._get_privateuse1_backend_name()
    device_mod = getattr(torch, device_type, None)
    if device_mod is None:
        reason = f"Skip as torch has no module of {device_type}"
        return unittest.skip(reason)(fn)
    return onlyOn(device_type)(fn)

