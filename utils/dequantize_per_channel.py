
def dequantize_per_channel(
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
    """Affine per channel dequantization for the Tensor using the same quantization
    parameters for each channel/axis to map from quantized values to floating point values

    Args:
       input (torch.Tensor): Tensor with dtype matching `dtype` argument,
       e.g. (`torch.uint8`), it is a per channel quantized Tensor if combined with
       quantization parameter in the argument of this function (scales/zero_points/axis)

       scales (torch.Tensor): a list of scale quantization parameter for
       affine quantization, one per channel

       zero_points (torch.Tensor): a list of zero_point quantization parameter for
       affine quantization, one per channel

       quant_min (int): minimum quantized value for output Tensor (not used in computation,
       reserved for pattern matching)

       quant_max (int): maximum quantized value for output Tensor (not used in computation,
       reserved for pattern matching)

       dtype (torch.dtype): requested dtype for output Tensor (not used in computation,
       reserved for pattern matching)

       out_dtype (torch.dtype?): optional dtype for output Tensor

    Returns:
       dequantized float32 Tensor
    """
    if input.dtype != dtype:
        raise AssertionError(
            f"Expecting input to have dtype: {dtype}, but got dtype: {input.dtype}"
        )
    if out_dtype is None:
        out_dtype = torch.float32
    if axis >= input.dim():
        raise AssertionError(f"Expecting axis to be < {input.dim()}")
    _quant_min_max_bounds_check(quant_min, quant_max, dtype)
    input, permute_axis_list = _permute_to_axis_zero(input, axis)

    new_shape = [1] * input.dim()
    new_shape[0] = scales.shape[0]
    scales = scales.view(new_shape)
    if zero_points is not None:
        res = (input - zero_points.view(new_shape)) * scales
    else:
        res = input * scales

    res = res.to(out_dtype)

    out = res.permute(tuple(permute_axis_list))
    return out

