
def _quantize_rowwise(x: Tensor, float8_dtype: torch.dtype):
    amax = torch.max(torch.abs(x), dim=1, keepdim=True).values
    scale = _amax_to_scale(amax, float8_dtype, x.dtype)
    x_fp8 = _to_fp8_saturated(x * scale, float8_dtype)
    inverse_scale = scale.reciprocal()
    return x_fp8, inverse_scale

