
def meta__scaled_dot_product_cudnn_attention(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    attn_bias: Tensor | None,
    compute_log_sumexp: bool,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    return_debug_mask: bool = False,
    scale: float | None = None,
):
    B = query.size(0)
    H = query.size(1)
    S_Q = query.size(2)
    S_KV = key.size(2)
    D_V = value.size(-1)

    res_shape = (B, H, S_Q, D_V)
    res = alloc_with_matching_layout(query, res_shape)

    logsum_exp = torch.empty(
        (B, H, S_Q, 1),
        dtype=torch.float,
        device=query.device,
    )

    # See Note [Seed and Offset]
    seed = torch.empty((), dtype=torch.long, device="meta")
    offset = torch.empty((), dtype=torch.long, device="meta")

    return (
        res,
        logsum_exp,
        None,
        None,
        S_Q,
        S_KV,
        seed,
        offset,
        None,
    )

