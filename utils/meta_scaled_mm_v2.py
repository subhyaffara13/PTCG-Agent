
def meta_scaled_mm_v2(
    self: torch.Tensor,
    mat2: torch.Tensor,
    scale_a: list[torch.Tensor],
    scale_recipe_a: list[ScalingType],
    swizzle_a: list[SwizzleType],
    scale_b: list[torch.Tensor],
    scale_recipe_b: list[ScalingType],
    swizzle_b: list[SwizzleType],
    bias: torch.Tensor | None = None,
    output_dtype: torch.dtype | None = None,
    contraction_dims: list[int] | None = None,
    use_fast_accum: bool = False,
):
    return _check_scaled_mm_sizes_v2(
        self,
        mat2,
        scale_a,
        scale_recipe_a,
        scale_b,
        scale_recipe_b,
        bias=bias,
        out_dtype=output_dtype,
        swizzle_a=swizzle_a,
        swizzle_b=swizzle_b,
        use_fast_accum=use_fast_accum,
    )

