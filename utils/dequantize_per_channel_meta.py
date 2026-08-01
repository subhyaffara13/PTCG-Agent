
def dequantize_per_channel_meta(
    input: torch.Tensor,
    scales: torch.Tensor,
    zero_points: torch.Tensor | None,
    axis: int,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    *,
    out_dtype: torch.dtype | None = None,
) -> torch.Tensor:
    if input.dtype != dtype:
        raise AssertionError(
            f"Expecting input to have dtype {dtype}, but got dtype: {input.dtype}"
        )
    if out_dtype is None:
        out_dtype = torch.float32
    if axis >= input.dim():
        raise AssertionError(f"Expecting axis to be < {input.dim()}")
    _quant_min_max_bounds_check(quant_min, quant_max, dtype)
    return torch.empty_like(input, dtype=out_dtype)

