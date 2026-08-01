
def meta__scaled_dot_product_flash_attention_for_cpu_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    dropout_p: float,
    is_causal: bool,
    attn_mask: Tensor | None = None,
    scale: float | None = None,
):
    # cpus's grad layout is different from cuda's,
    # i.e. (batch_size, seq_len, num_heads, head_dim)
    grad_q = torch.empty_permuted(
        query.size(),
        (0, 2, 1, 3),
        dtype=query.dtype,
        device=query.device,
    )
    grad_k = torch.empty_permuted(
        key.size(),
        (0, 2, 1, 3),
        dtype=key.dtype,
        device=key.device,
    )
    grad_v = torch.empty_permuted(
        value.size(),
        (0, 2, 1, 3),
        dtype=value.dtype,
        device=value.device,
    )

    return grad_q, grad_k, grad_v

