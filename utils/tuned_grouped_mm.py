
def tuned_grouped_mm(
    mat_a: TensorBox,
    mat_b: TensorBox,
    offs: TensorBox | None = None,
    bias: TensorBox | None = None,
    out_dtype: torch.dtype | None = None,
    layout: Layout | None = None,
) -> TensorBox:
    """Auto-tuning for _grouped_mm() operator."""

    return _tuned_grouped_mm_common(
        "aten._grouped_mm.default",
        "grouped_mm",
        aten__grouped_mm,
        triton_grouped_mm_template,
        mat_a,
        mat_b,
        None,
        None,
        offs,
        bias,
        None,
        out_dtype,
        None,
        layout,
    )

