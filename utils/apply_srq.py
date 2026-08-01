
def apply_srq(x: torch.Tensor, scale: torch.Tensor, bits: int = 8) -> torch.Tensor:
    """Apply Static Range Quantization rounding and clipping (in x's dtype).

    A `scale` of 0 means the layer is uncalibrated, in which case this is a no-op. The guard uses
    `torch.where` rather than `scale.item()` so it stays on-device and `torch.compile`-friendly (an
    `.item()` would force a host-device sync and break `fullgraph=True`).
    """
    scale = scale.to(x.dtype)
    max_value = 2 ** (bits - 1) - 1
    min_value = -max_value - 1
    calibrated = scale != 0
    safe_scale = torch.where(calibrated, scale, torch.ones_like(scale))
    x_q = torch.clamp(torch.round(x / safe_scale), float(min_value), float(max_value)) * safe_scale
    return torch.where(calibrated, x_q, x)

