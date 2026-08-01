
def restride_A_for_fused_matmul_reduce_scatter(
    t: torch.Tensor,
    scatter_dim: int,
) -> torch.Tensor:
    """
    Restride the `A_shard` arg of `fused_matmul_reduce_scatter` for optimal
    perf. See the doc for `fused_matmul_reduce_scatter` for detail.
    """
    perm = list(range(len(t.shape)))
    perm.insert(0, perm.pop(scatter_dim))
    return make_contiguous_for_perm(t, perm)

