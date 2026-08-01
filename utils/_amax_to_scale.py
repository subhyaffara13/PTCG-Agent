
def _amax_to_scale(
    amax: torch.Tensor, float8_dtype: torch.dtype, orig_dtype: torch.dtype
) -> torch.Tensor:
    # To make scale dtype to be fp32 for accuracy
    amax = amax.float()
    if float8_dtype == torch.float8_e4m3fn:
        res = E4M3_MAX_POS / torch.clamp(amax, min=EPS)
    else:  # e5m2
        res = E5M2_MAX_POS / torch.clamp(amax, min=EPS)

    # Ensure that the scale is representable in float16,
    # this helps when amax is small. We are assuming that we don't need
    # to care about this for float32/bfloat16.
    if orig_dtype is torch.float16:
        res = torch.clamp(res, max=FP16_MAX_POS)
    return res

