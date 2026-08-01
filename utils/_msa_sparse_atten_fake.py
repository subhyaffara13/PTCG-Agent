
def _msa_sparse_atten_fake(
    q,
    k,
    v,
    q2k,
    cu_seqlens_q,
    cu_seqlens_k,
    topk,
    block_size,
    total_k,
    max_seqlen_q,
    max_seqlen_k,
    qheads_per_kv,
    scaling,
    impl,
):
    # Output matches the query varlen layout [total_q, Hq, head_dim].
    return torch.empty_like(q)

