
def meta_grouped_mm(
    mat_a: Tensor,
    mat_b: Tensor,
    offs: Tensor | None = None,
    bias: Tensor | None = None,
    out_dtype: torch.dtype | None = None,
) -> Tensor:
    return _meta_grouped_mm_common(
        mat_a,
        mat_b,
        scale_a=None,
        scale_b=None,
        offs=offs,
        bias=bias,
        scale_result=None,
        out_dtype=out_dtype,
    )

