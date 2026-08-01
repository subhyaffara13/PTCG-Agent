
def dequantize_per_channel_group(
    w_int8: torch.Tensor,
    scales: torch.Tensor,
    zero_points: torch.Tensor | None,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    group_size: int = 128,
    output_dtype: torch.dtype = torch.float32,
):
    """Groupwise dequantization within each channel for an 2-d Tensor using the quantization parameters
    to map from floating point to quantized values. This means for each row of a 2-d Tensor
    (M, N), we calculate scales/zero_points for each `group_size` elements
    and quantize every `group_size` elements with the same quantization parameter.
    The dimension for scales/zero_points will be (M * ceil(N, group_size),)

    Args:
       input (torch.Tensor): quantized Tensor (uint8/int8 etc.)
       scales (float32 torch.Tensor): quantization parameter for per channel group affine quantization
       zero_points (int32 torch.Tensor): quantization parameter for per channel group affine quantization
       quant_min (int): minimum quantized value for input Tensor
       quant_max (int): maximum quantized value for input Tensor
       dtype (torch.dtype): dtype (e.g. torch.uint8) for input Tensor
       output_dtype (torch.dtype): dtype (e.g. torch.float32) for output Tensor

    Returns:
       dequantized Tensor with dtype `output_dtype`
    """

    if group_size <= 1:
        raise AssertionError("group_size must be > 1")
    # needed for GPTQ single column dequantize
    if group_size > w_int8.shape[-1] and scales.shape[-1] == 1:
        group_size = w_int8.shape[-1]
    if w_int8.shape[-1] % group_size != 0:
        raise AssertionError("w_int8.shape[-1] must be divisible by group_size")
    if w_int8.dim() != 2:
        raise AssertionError("w_int8 must be 2-dimensional")

    w_int8_grouped = w_int8.reshape(-1, group_size)
    scales = scales.reshape(-1, 1)
    if zero_points is not None:
        zp = zero_points.reshape(-1, 1)
    else:
        zp = torch.zeros([], dtype=torch.int32, device=scales.device)
    w_dq = w_int8_grouped.sub(zp).mul(scales).reshape_as(w_int8).to(output_dtype)
    return w_dq

