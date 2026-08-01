
def _device_put_meta(
    a: TensorLikeType, device: str | torch.device, non_blocking=False
) -> TensorLikeType:
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")  # mypy
    if not isinstance(device, (str, torch.device)):
        raise AssertionError(f"device must be str or torch.device, got {type(device)}")
    if not isinstance(non_blocking, bool):
        raise AssertionError(f"non_blocking must be bool, got {type(non_blocking)}")

    return TensorMeta(a, device=utils.canonicalize_device(device))

