
def _insert_fused_matmul_reduce_scatter(
    graph: torch.fx.Graph,
    matmul: _Matmul,
    reduce_op: str,
    orig_scatter_dim: int,
    group_name: "torch.distributed.distributed_c10d.GroupName",
    scatter_dim_after_reshape: int,  # only used for reshape -> scaled_mm -> reshape pattern
    output_shape: list[int],  # only used for reshape -> scaled_mm -> reshape pattern
) -> torch.fx.Node:
    if type(matmul) is _Matmul:
        return graph.call_function(
            torch.ops.symm_mem.fused_matmul_reduce_scatter.default,
            args=(
                matmul.A_node,
                matmul.B_node,
                reduce_op,
                orig_scatter_dim,
                group_name,
            ),
        )
    elif type(matmul) is _ScaledMatmul:
        return graph.call_function(
            torch.ops.symm_mem.fused_scaled_matmul_reduce_scatter.default,
            args=(
                matmul.A_node,
                matmul.B_node,
                matmul.A_scale_node,
                matmul.B_scale_node,
                reduce_op,
                orig_scatter_dim,
                scatter_dim_after_reshape,
                group_name,
                output_shape,
                matmul.bias_node,
                matmul.result_scale_node,
                matmul.out_dtype,
                matmul.use_fast_accum,
            ),
        )
    else:
        raise AssertionError(f"Unexpected matmul match type: {type(matmul)}")

