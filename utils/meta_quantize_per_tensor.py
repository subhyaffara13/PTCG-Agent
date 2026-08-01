
def meta_quantize_per_tensor(
    input: torch.Tensor, scale: float, zero_point: int, dtype: torch.dtype
) -> torch.Tensor:
    return torch.empty_like(input)

