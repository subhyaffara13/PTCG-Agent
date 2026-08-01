
def meta__scaled_dot_product_efficient_attention(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    attn_bias: Tensor | None,
    compute_log_sumexp: bool,
    dropout_p=0.0,
    is_causal: bool = False,
    scale: float | None = None,
):
    query = query.transpose(1, 2)
    key = key.transpose(1, 2)
    value = value.transpose(1, 2)

    B = query.size(0)
    M = query.size(1)
    num_heads = query.size(-2)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    if torch.version.hip and torch.cuda.is_available():
        """Please see: https://github.com/pytorch/pytorch/issues/146848
        longsumexp last dim should be seq length
        """
        logsumexp_dim = M if compute_log_sumexp else 0
    else:
        logsumexp_dim = math.ceil(M / 32) * 32 if compute_log_sumexp else 0

    logsum_exp = torch.empty(
        (B, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    res = res.transpose(1, 2)

    # See Note [Seed and Offset]:
    seed = torch.empty((), dtype=torch.long, device="meta")
    offset = torch.empty((), dtype=torch.long, device="meta")

    return res, logsum_exp, seed, offset

