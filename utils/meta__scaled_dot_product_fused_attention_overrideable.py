
def meta__scaled_dot_product_fused_attention_overrideable(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    attn_bias: Tensor | None = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    return_debug_mask: bool = False,
    scale: float | None = None,
):
    # Explicitly handle 3D (H, S, D) and 4D (B, H, S, D) inputs,
    # matching the C++ runtime in aten_mtia_ops.cpp.
    B, H_Q, S_Q = 0, 0, 0
    if query.dim() == 4:
        B, H_Q, S_Q, _ = query.size()
    elif query.dim() == 3:
        H_Q, S_Q, _ = query.size()
        B = 1
    else:
        raise RuntimeError("query must be 3D or 4D")
    S_KV = key.size(-2)
    D_V = value.size(-1)

    # Preserve input dimensionality for the output shape
    out_shape = list(query.shape)
    out_shape[-1] = D_V
    res = alloc_with_matching_layout(query, tuple(out_shape))

    logsum_exp = torch.empty(
        (B, H_Q, S_Q),
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

