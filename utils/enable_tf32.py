
def enable_tf32(enable: bool) -> None:
    """
    Set TF32 mode using the appropriate PyTorch API.
    For PyTorch 2.9+, uses the new fp32_precision API.
    For older versions, uses the legacy allow_tf32 flags.
    Args:
        enable: Whether to enable TF32 mode
    """
    import torch

    pytorch_version = version.parse(get_torch_version())
    if pytorch_version >= version.parse("2.9.0"):
        precision_mode = "tf32" if enable else "ieee"
        if hasattr(torch.backends, "fp32_precision"):
            torch.backends.fp32_precision = precision_mode
    else:
        if is_torch_musa_available():
            if hasattr(torch.backends, "mudnn"):
                torch.backends.mudnn.allow_tf32 = enable
        else:
            torch.backends.cuda.matmul.allow_tf32 = enable
            torch.backends.cudnn.allow_tf32 = enable

