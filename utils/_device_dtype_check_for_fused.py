
def _device_dtype_check_for_fused(
    p: torch.Tensor, cuda_unsupported: bool = False
) -> None:
    fused_supported_devices = _get_fused_kernels_supported_devices()
    if cuda_unsupported:
        fused_supported_devices.remove("cuda")
    if not (p.device.type in fused_supported_devices and torch.is_floating_point(p)):
        raise RuntimeError(
            "`fused=True` requires all the params to be floating point Tensors of "
            f"supported devices: {fused_supported_devices} but {p.dtype} and {p.device.type}"
        )

