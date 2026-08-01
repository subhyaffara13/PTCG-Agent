
def finegrained_fp8_linear(
    input: torch.Tensor,
    weight: torch.Tensor,
    weight_scale_inv: torch.Tensor,
    block_size: list[int] | None = None,
    bias: torch.Tensor | None = None,
    activation_scale: torch.Tensor | None = None,
    output_dtype: torch.dtype | None = None,
) -> torch.Tensor:
    """Triton FP8/FP4 linear: fused act-quant + matmul, then optional bias add.

    ``activation_scale=None`` → dynamic per-K-block scales (inline); set it for
    static per-tensor quant. ``weight_scale_inv`` accepts fp32 or UE8M0; the
    dispatcher routes FP4 (``int8``-packed) weights automatically.
    """
    finegrained_fp8 = load_finegrained_fp8_kernel()
    output = finegrained_fp8.matmul(
        input,
        weight,
        weight_scale_inv,
        block_size,
        output_dtype,
        activation_scale=activation_scale,
    )
    if bias is not None:
        output.add_(bias)
    return output

