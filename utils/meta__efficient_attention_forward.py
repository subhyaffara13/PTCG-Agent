
def meta__efficient_attention_forward(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    bias: Tensor | None,
    cu_seqlens_q: Tensor | None,
    cu_seqlens_k: Tensor | None,
    max_seqlen_q: int | None,
    max_seqlen_k: int | None,
    dropout_p: float,
    custom_mask_type: int,
    compute_log_sumexp: bool = False,
    scale: float | None = None,
    causal_diagonal: Tensor | None = None,
    seqlen_k: Tensor | None = None,
    window_size: int | None = None,
):
    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    num_heads = query.size(-2)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    logsumexp_batch_dim = cu_seqlens_q.size(0) - 1 if (cu_seqlens_q is not None) else B
    actual_max_seqlen_q = M
    if cu_seqlens_q is not None:
        if max_seqlen_q is None:
            raise AssertionError(
                "max_seqlen_q must not be None when cu_seqlens_q is provided"
            )
        actual_max_seqlen_q = max_seqlen_q
    actual_max_seqlen_k = max_seqlen_k if max_seqlen_k is not None else N
    logsumexp_dim = (
        math.ceil(actual_max_seqlen_q / 32) * 32 if compute_log_sumexp else 0
    )
    logsum_exp = torch.empty(
        (logsumexp_batch_dim, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    # See Note [Seed and Offset]:
    seed = torch.empty((), dtype=torch.long, device="meta")
    offset = torch.empty((), dtype=torch.long, device="meta")

    return res, logsum_exp, seed, offset, actual_max_seqlen_q, actual_max_seqlen_k

