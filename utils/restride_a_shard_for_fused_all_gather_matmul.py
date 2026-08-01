
def restride_A_shard_for_fused_all_gather_matmul(
    t: torch.Tensor,
    gather_dim: int,
) -> torch.Tensor:
    """
    Restride the `A_shard` arg of `fused_all_gather_matmul` for optimal perf.
    See the doc for `fused_all_gather_matmul` for detail.
    """
    perm = list(range(len(t.shape)))
    perm.insert(0, perm.pop(gather_dim))
    return make_contiguous_for_perm(t, perm)

