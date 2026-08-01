
def dequantize_per_tensor_tensor2(
    input: torch.Tensor,
    scale: torch.Tensor,
    zero_point: torch.Tensor,
    quant_min: torch.Tensor,
    quant_max: torch.Tensor,
    dtype: torch.dtype,
    *,
    out_dtype: torch.dtype | None = None,
) -> torch.Tensor:
    """Affine dequantization for the Tensor using the same quantization parameters to map
    from quantized values to floating point values
    Same as `dequantize_per_tensor` but scale and zero_point are Scalar Tensor instead of
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
    return dequantize_per_tensor(
        input,
        scale.item(),
        zero_point.item(),  # type: ignore[arg-type]
        quant_min.item(),  # type: ignore[arg-type]
        quant_max.item(),  # type: ignore[arg-type]
        dtype,
        out_dtype=out_dtype,
    )

