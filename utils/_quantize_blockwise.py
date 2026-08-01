
def _quantize_blockwise(
    x: Tensor, float8_dtype: torch.dtype, block_outer: int, block_inner: int
):
    min_outer = min(block_outer, x.shape[0])
    min_inner = min(block_inner, x.shape[1])
    x = x.unflatten(1, (-1, min_inner)).unflatten(0, (-1, min_outer))
    amax = x.abs().amax(dim=[1, 3], keepdim=True).float()
    scale = _amax_to_scale(amax, float8_dtype, x.dtype)
    x = x.flatten(2, 3).flatten(0, 1)
    scale = scale.flatten(2, 3).flatten(0, 1)
    scale_expanded = scale.repeat_interleave(min_outer, dim=0).repeat_interleave(
        min_inner, dim=1
    )
    x_fp8 = _to_fp8_saturated(
        x / scale_expanded,  # Ensures that scaling doesn't cause inf/nan values
        float8_dtype,
    )
    inverse_scale = scale.reciprocal()
    return x_fp8, inverse_scale

