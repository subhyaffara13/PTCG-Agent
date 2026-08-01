
def meta_scaled_grouped_mm(
    mat_a: torch.Tensor,
    mat_b: torch.Tensor,
    scale_a: torch.Tensor,
    scale_b: torch.Tensor,
    offs: torch.Tensor | None = None,
    bias: torch.Tensor | None = None,
    scale_result: torch.Tensor | None = None,
    out_dtype: torch.dtype | None = None,
    use_fast_accum: bool = False,
):
    # matching _scaled_grouped_mm_cuda Blas.cpp implementation
    out_dtype = out_dtype or torch.bfloat16

    return _meta_grouped_mm_common(
        mat_a,
        mat_b,
        scale_a=scale_a,
        scale_b=scale_b,
        offs=offs,
        bias=bias,
        scale_result=scale_result,
        out_dtype=out_dtype,
        use_fast_accum=use_fast_accum,
    )

