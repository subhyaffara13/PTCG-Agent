
def meta__scaled_dot_product_efficient_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    attn_bias: Tensor | None,
    out: Tensor,
    logsumexp: Tensor,
    philox_seed: Tensor,
    philox_offset: Tensor,
    dropout_p: float,
    grad_input_mask: list[bool],
    is_causal: bool = False,
    scale: float | None = None,
):
    batch_size = query.size(0)
    num_heads = query.size(1)
    max_q = query.size(2)
    head_dim = query.size(3)
    head_dim_v = value.size(3)

    max_k = key.size(2)

    grad_q = torch.empty_permuted(
        (batch_size, num_heads, max_q, head_dim),
        (0, 2, 1, 3),
        dtype=query.dtype,
        device=query.device,
    )
    grad_k = torch.empty_permuted(
        (batch_size, num_heads, max_k, head_dim),
        (0, 2, 1, 3),
        dtype=key.dtype,
        device=key.device,
    )
    grad_v = torch.empty_permuted(
        (batch_size, num_heads, max_k, head_dim_v),
        (0, 2, 1, 3),
        dtype=value.dtype,
        device=value.device,
    )
    grad_bias = None
    if attn_bias is not None and grad_input_mask[3]:
        lastDim = attn_bias.size(-1)
        lastDimAligned = lastDim if lastDim % 16 == 0 else lastDim + 16 - lastDim % 16
        new_sizes = list(attn_bias.size())
        new_sizes[-1] = lastDimAligned
        grad_bias = torch.empty(
            new_sizes, dtype=attn_bias.dtype, device=attn_bias.device
        )
        grad_bias = grad_bias[..., :lastDim]

    return grad_q, grad_k, grad_v, grad_bias

