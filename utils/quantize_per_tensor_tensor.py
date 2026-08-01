
def quantize_per_tensor_tensor(
    input: torch.Tensor,
    scale: torch.Tensor,
    zero_point: torch.Tensor,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
) -> torch.Tensor:
    """Affine quantization for the Tensor using the same quantization parameters to map
    from floating point to quantized values
    Same as `quantize_per_tensor` but scale and zero_point are Scalar Tensor instead of
    scalar values
    """
    if zero_point.numel() != 1:
        raise AssertionError(
            f"Expecting zero_point tensor to be one element, but received : {zero_point.numel()}"
        )
    if scale.numel() != 1:
        raise AssertionError(
            f"Expecting scale tensor to be one element, but received : {scale.numel()}"
        )
    return quantize_per_tensor(
        input,
        scale.item(),
        zero_point.item(),  # type: ignore[arg-type]
        quant_min,  # type: ignore[arg-type]
        quant_max,  # type: ignore[arg-type]
        dtype,
    )

