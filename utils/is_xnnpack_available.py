
def is_xnnpack_available():
    if TORCH_AVAILABLE:
        import torch.backends.xnnpack

        return str(torch.backends.xnnpack.enabled)  # type: ignore[attr-defined]
    else:
        return "N/A"

