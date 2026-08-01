
def _maybe_contiguous(x: torch.Tensor | None) -> torch.Tensor | None:
    """Ensure tensor is contiguous in the last dimension."""
    return x.contiguous() if x is not None and x.stride(-1) != 1 else x

