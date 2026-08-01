
def _warn_tf32_disabled() -> None:
    if (
        torch.cuda.is_available()
        and torch.backends.cuda.matmul.fp32_precision != "tf32"
        and torch.cuda.get_device_capability() >= (8, 0)
    ):
        warnings.warn(
            "TensorFloat32 tensor cores for float32 matrix multiplication available but not enabled. "
            "Consider setting `torch.set_float32_matmul_precision('high')` for better performance."
        )


def _warn_tf32_disabled() -> None:
    if (
        torch.cuda.is_available()
        and torch.backends.cuda.matmul.fp32_precision != "tf32"
        and torch.cuda.get_device_capability() >= (8, 0)
    ):
        warnings.warn(
            "TensorFloat32 tensor cores for float32 matrix multiplication available but not enabled. "
            "Skipping pattern matching to fused flash-attention. "
            "Consider setting `torch.set_float32_matmul_precision('high')` for better performance."
        )

