
def quantize_per_channel(
    input: torch.Tensor,
    scales: torch.Tensor,
    zero_points: torch.Tensor,
    axis: int,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
) -> torch.Tensor:
    """Affine per channel quantization for the Tensor using the same quantization
    parameters for each channel/axis to map from floating point to quantized values

    Args:
       input (torch.Tensor): original float32 or bfloat16 Tensor
       scales (torch.Tensor): a list of scale quantization parameter for
       affine quantization, one per channel
       zero_point (torch.Tensor): a list of zero_point quantization parameter for
       affine quantization, one per channel
       quant_min (int): minimum quantized value for output Tensor
       quant_max (int): maximum quantized value for output Tensor
       dtype (torch.dtype): requested dtype (e.g. torch.uint8) for output Tensor

    Returns:
       Tensor with requested dtype (e.g. torch.uint8), note the quantization parameters
       are not stored in the Tensor, we are storing them in function arguments instead
    """
    if input.dtype in [torch.float16, torch.bfloat16]:
        input = input.to(torch.float32)
    if input.dtype != torch.float32:
        raise AssertionError(
            f"Expecting input to have dtype torch.float32, but got dtype: {input.dtype}"
        )
    if axis >= input.dim():
        raise AssertionError(f"Expecting axis to be < {input.dim()}")
    _quant_min_max_bounds_check(quant_min, quant_max, dtype)
    input, permute_axis_list = _permute_to_axis_zero(input, axis)

    new_shape = [1] * input.dim()
    new_shape[0] = scales.shape[0]
    scales = scales.view(new_shape)
    zero_points = zero_points.view(new_shape)

    res = torch.clamp(
        torch.round(input * (1.0 / scales)) + zero_points, quant_min, quant_max
    )
    out = res.permute(tuple(permute_axis_list))
    return out.to(dtype)

