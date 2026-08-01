
def tuned_scaled_grouped_mm(
    mat_a: TensorBox,
    mat_b: TensorBox,
    scale_a: TensorBox,
    scale_b: TensorBox,
    offs: TensorBox | None = None,
    bias: TensorBox | None = None,
    scale_result: TensorBox | None = None,
    out_dtype: torch.dtype | None = None,
    use_fast_accum: bool = False,
    layout: Layout | None = None,
) -> TensorBox:
    """Auto-tuning for _scaled_grouped_mm() operator."""

    # matching _scaled_grouped_mm_cuda Blas.cpp implementation
    out_dtype = out_dtype or torch.bfloat16

    return _tuned_grouped_mm_common(
        "aten._scaled_grouped_mm.default",
        "scaled_grouped_mm",
        aten__scaled_grouped_mm,
        triton_scaled_grouped_mm_template,
        mat_a,
        mat_b,
        scale_a,
        scale_b,
        offs,
        bias,
        scale_result,
        out_dtype,
        use_fast_accum,
        layout,
    )

