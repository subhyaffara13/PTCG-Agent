
def _grouped_mm_fallback_fake(input: torch.Tensor, weight: torch.Tensor, offs: torch.Tensor) -> torch.Tensor:
    """Shape/dtype inference stub for `_grouped_mm_fallback` required by `torch.compile`."""
    assert input.dim() == 2, f"input must be 2D (S, input_dim), got shape {tuple(input.shape)}"
    assert weight.dim() == 3, (
        f"weight must be 3D (num_experts, input_dim, output_dim), got shape {tuple(weight.shape)}"
    )
    assert offs.dim() == 1, f"offs must be 1D (num_experts,), got shape {tuple(offs.shape)}"
    assert offs.size(0) == weight.size(0), f"offs length {offs.size(0)} must match number of experts {weight.size(0)}"
    assert input.size(1) == weight.size(1), (
        f"input_dim mismatch: input has {input.size(1)}, weight has {weight.size(1)}"
    )
    assert offs.dtype in (torch.int32, torch.int64), f"offs must be an integer tensor, got {offs.dtype}"
    return torch.empty(input.size(0), weight.size(2), device=input.device, dtype=input.dtype)

