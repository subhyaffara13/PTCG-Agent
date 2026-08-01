
def _apply_norm(
    x: TensorLikeType, norm: NormType, signal_numel: int, forward: bool
) -> TensorLikeType:
    """Apply normalization to the un-normalized FFT result"""
    torch._check(norm in _NORM_VALUES, lambda: f"Invalid normalization mode: {norm}")

    if norm == "ortho":
        return x * (1 / math.sqrt(signal_numel))

    normalize = (not forward and (norm is None or norm == "backward")) or (
        forward and norm == "forward"
    )
    return x * (1 / signal_numel) if normalize else x

