
def copy_to(a: Tensor, b: Tensor, *, allow_cross_device=True):
    if not allow_cross_device and a.device != b.device:
        msg = f"Attempting to copy from device {b.device} to device {a.device}, but cross-device copies are not allowed!"
        raise RuntimeError(msg)

    return prims.copy_to(a, b)

