
def meta__scaled_dot_product_fused_attention_overrideable_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    attn_bias: Tensor,
    grad_input_mask: list[bool],
    out: Tensor,
    logsumexp: Tensor,
    cum_seq_q: Tensor,
    cum_seq_k: Tensor,
    max_q: int,
    max_k: int,
    dropout_p: float,
    is_causal: bool,
    philox_seed: Tensor,
    philox_offset: Tensor,
    *,
    scale: float | None = None,
):
    grad_q = torch.empty_like(query)
    grad_k = torch.empty_like(key)
    grad_v = torch.empty_like(value)
    grad_attn_bias = torch.empty_like(attn_bias) if attn_bias is not None else None
    return grad_q, grad_k, grad_v, grad_attn_bias

