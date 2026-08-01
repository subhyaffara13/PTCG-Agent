
def _fused_matmul_reduce_scatter(
    A: torch.Tensor,
    B: torch.Tensor,
    reduce_op: str,
    scatter_dim: int,
    group_name: c10d.GroupName,
) -> torch.Tensor:
    """
    Perform the following logic with micro-pipelined computation and
    communication:

        reduce_scatter_tensor(A @ B, reduce_op, scatter_dim, group_name)

    Optimal stride order for A - if A.movedim(scatter_dim, 0) is contiguous, no
    extra copy is required for input layout transformation. Otherwise A needs
    to be copied once.
    """
    if _is_test_mode:
        return _fused_matmul_reduce_scatter_fallback(
            A, B, reduce_op, scatter_dim, group_name
        )

    with torch.profiler.record_function("fused_matmul_reduce_scatter"):
        return _fused_matmul_reduce_scatter_impl(
            mm_out_op=torch.ops.aten.mm.out,
            A=A,
            B=B,
            kwargs={},
            out_dtype=A.dtype,
            reduce_op=reduce_op,
            scatter_dim=scatter_dim,
            group_name=group_name,
        )

