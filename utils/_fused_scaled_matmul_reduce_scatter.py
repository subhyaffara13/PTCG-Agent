
def _fused_scaled_matmul_reduce_scatter(
    A: torch.Tensor,
    B: torch.Tensor,
    A_scale: torch.Tensor,
    B_scale: torch.Tensor,
    reduce_op: str,
    orig_scatter_dim: int,
    scatter_dim_after_maybe_reshape: int,
    group_name: c10d.GroupName,
    output_shape: list[int],
    bias: torch.Tensor | None = None,
    result_scale: torch.Tensor | None = None,
    out_dtype: torch.dtype | None = None,
    use_fast_accum: bool = False,
) -> torch.Tensor:
    if _is_test_mode:
        return _fused_scaled_matmul_reduce_scatter_fallback(
            A,
            B,
            A_scale,
            B_scale,
            reduce_op,
            orig_scatter_dim,
            scatter_dim_after_maybe_reshape,
            group_name,
            output_shape,
            bias,
            result_scale,
            out_dtype,
            use_fast_accum,
        )
    with torch.profiler.record_function("fused_scaled_matmul_reduce_scatter"):
        return _fused_scaled_matmul_reduce_scatter_impl(
            mm_out_op=torch.ops.aten._scaled_mm.out,
            A=A,
            B=B,
            A_scale=A_scale,
            kwargs={
                "scale_b": B_scale,
                "bias": bias,
                "scale_result": result_scale,
                "out_dtype": out_dtype,
                "use_fast_accum": use_fast_accum,
            },
            out_dtype=out_dtype,
            reduce_op=reduce_op,
            orig_scatter_dim=orig_scatter_dim,
            scatter_dim_after_maybe_reshape=scatter_dim_after_maybe_reshape,
            group_name=group_name,
            output_shape=output_shape,
        )

