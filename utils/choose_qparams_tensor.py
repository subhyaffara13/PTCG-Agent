
def choose_qparams_tensor(
    input: torch.Tensor,
    quant_min: int,
    quant_max: int,
    eps: float,
    dtype: torch.dtype,
) -> tuple[torch.Tensor, torch.Tensor]:
    min_val, max_val = torch.aminmax(input)
    scale = (max_val - min_val) / float(quant_max - quant_min)
    scale = torch.max(scale, torch.Tensor([eps]))
    zero_point = quant_min - torch.round(min_val / scale).to(torch.int)
    zero_point = torch.clamp(zero_point, quant_min, quant_max)
    return scale.to(torch.float64), zero_point.to(torch.int64)


def choose_qparams_tensor(
    input: torch.Tensor, qmin: int, qmax: int, eps: float, dtype: torch.dtype
) -> tuple[torch.Tensor, torch.Tensor]:
    """Given an input Tensor, derive the per tensor affine quantization parameter
    (scale and zero_point) for target quantized Tensor from the Tensor

    Args:
       input (torch.Tensor): floating point input Tensor
       quant_min (int): minimum quantized value for target quantized Tensor
       quant_max (int): maximum quantized value for target quantized Tensor
       dtype (torch.dtype): dtype for target quantized Tensor

    Returns:
       scale (float): quantization parameter for the target quantized Tensor
       zero_point (int): quantization parameter for the target quantized Tensor
    """
    if input.dtype not in [
        torch.float32,
        torch.float16,
        torch.bfloat16,
    ]:
        raise AssertionError(
            f"Expecting input to have dtype torch.float32/16/b16, but got dtype: {input.dtype}"
        )
    if dtype not in _DTYPE_TO_QVALUE_BOUNDS:
        raise AssertionError(
            f"Expecting target dtype to be one of {_DTYPE_TO_QVALUE_BOUNDS.keys()}, but got: {dtype}"
        )
    validate_qmin_qmax(qmin, qmax)

    min_val, max_val = torch.aminmax(input)

    return determine_qparams(
        min_val,
        max_val,
        qmin,
        qmax,
        dtype,
        torch.Tensor([eps]),
        has_customized_qrange=False,
    )

