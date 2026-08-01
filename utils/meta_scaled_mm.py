
def meta_scaled_mm(
    self: torch.Tensor,
    mat2: torch.Tensor,
    scale_a: torch.Tensor,
    scale_b: torch.Tensor,
    bias: torch.Tensor | None = None,
    scale_result: torch.Tensor | None = None,
    out_dtype: torch.dtype | None = None,
    use_fast_accum: bool = False,
):
    return _check_scaled_mm_sizes(
        self, mat2, scale_a, scale_b, bias, scale_result, out_dtype, use_fast_accum
    )

