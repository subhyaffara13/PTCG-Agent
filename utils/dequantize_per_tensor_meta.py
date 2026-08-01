
def dequantize_per_tensor_meta(
    input: torch.Tensor,
    scale: torch.Tensor,
    zero_point: torch.Tensor,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    *,
    out_dtype: torch.dtype | None = None,
) -> torch.Tensor:
    if out_dtype is None:
        out_dtype = torch.float32
    return torch.empty_like(input, dtype=out_dtype)

