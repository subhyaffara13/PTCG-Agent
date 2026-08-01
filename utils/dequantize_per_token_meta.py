
def dequantize_per_token_meta(
    input: torch.Tensor,
    scales: torch.Tensor,
    zero_points: torch.Tensor,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    output_dtype: torch.dtype = torch.float32,
):
    _quant_min_max_bounds_check(quant_min, quant_max, dtype)
    # TODO: support fp16
    return torch.empty_like(input, dtype=output_dtype)

