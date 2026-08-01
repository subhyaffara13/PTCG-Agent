
def quantize_per_tensor_tensor2_meta(
    input: torch.Tensor,
    scale: torch.Tensor,
    zero_point: torch.Tensor,
    quant_min: torch.Tensor,
    quant_max: torch.Tensor,
    dtype: torch.dtype,
) -> torch.Tensor:
    return quantize_per_tensor_tensor_meta(
        input,
        scale,
        zero_point,  # type: ignore[arg-type]
        quant_min,  # type: ignore[arg-type]
        quant_max,  # type: ignore[arg-type]
        dtype,
    )

