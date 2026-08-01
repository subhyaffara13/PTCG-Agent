
def _get_torch_and_device():
    global _TORCH_DEVICE
    global _TORCH_HAS_TENSORDOT

    if _TORCH_DEVICE is None:
        import torch  # type: ignore

        device = "cuda" if torch.cuda.is_available() else "cpu"
        _TORCH_DEVICE = torch, device
        _TORCH_HAS_TENSORDOT = hasattr(torch, "tensordot")

    return _TORCH_DEVICE

