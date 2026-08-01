
def _fused_all_gather_matmul(
    A_shard: torch.Tensor,
    Bs: list[torch.Tensor],
    gather_dim: int,
    group_name: c10d.GroupName,
    *,
    return_A: bool = True,
) -> tuple[torch.Tensor | None, list[torch.Tensor]]:
    """
    Perform the following logic with micro-pipelined computation and
    communication:

        all_gather_tensor(A_shard, gather_dim, group_name) @ B

    Optimal stride order for A_shard - if A_shard.movedim(gather_dim, 0) is
    contiguous, no extra copy is required for input layout transformation.
    Otherwise A_shard needs to be copied once.
    """
    if _is_test_mode:
        return _fused_all_gather_matmul_fallback(
            A_shard, Bs, gather_dim, group_name, return_A=return_A
        )

    if _should_use_fused_all_gather_matmul_native(A_shard, Bs, gather_dim, group_name):
        group = c10d._resolve_process_group(group_name)
        leading_dims = list(A_shard.shape[:-1])
        leading_dims[0] *= group.size()
        A, out = _fused_all_gather_matmul_native(
            A_shard.flatten(0, -2), Bs[0], group_name
        )
        return A.view(*leading_dims, -1), [out.view(*leading_dims, -1)]

    if _should_use_multimem_all_gather_matmul(
        A_shard, gather_dim, group_name, return_A
    ):
        return None, _multimem_all_gather_matmul(A_shard, Bs, group_name)

    with torch.profiler.record_function("fused_all_gather_matmul"):
        return _fused_all_gather_matmul_impl(
            torch.ops.aten.mm.out,
            A_shard,
            Bs,
            None,
            [{} for B in Bs],
            [B.dtype for B in Bs],
            gather_dim,
            group_name,
            return_A,
        )

