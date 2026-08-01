
def check_copy_devices(*, copy_from: TensorLikeType, copy_to: TensorLikeType) -> None:
    if copy_from.device != copy_to.device:
        msg = (
            f"Attempting to copy from device {copy_from.device} "
            f"to device {copy_to.device}, but cross-device copies are not allowed!"
        )
        raise RuntimeError(msg)

