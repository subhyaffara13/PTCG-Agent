
def _fa4_scaled_dot_product_flash_attention_backward_impl(
    grad_out: torch.Tensor,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    logsumexp: torch.Tensor,
    cum_seq_q: torch.Tensor | None,
    cum_seq_k: torch.Tensor | None,
    max_q: int,
    max_k: int,
    dropout_p: float,
    is_causal: bool,
    philox_seed: torch.Tensor,
    philox_offset: torch.Tensor,
    *,
    scale: float | None = None,
):
    error = _fa4_backward_support_error(
        grad_out,
        query,
        key,
        value,
        out,
        logsumexp,
        dropout_p,
        None,
    )
    if error is not None:
        raise RuntimeError(f"FA4 SDPA backward unsupported: {error}")
    q, k, v, o, go = _transpose_dense(query, key, value, out, grad_out)
    max_q = query.size(2)
    max_k = key.size(2)
    dq, dk, dv = _fa4_flash_attention_backward_impl(
        go,
        q,
        k,
        v,
        o,
        logsumexp,
        None,
        None,
        max_q,
        max_k,
        dropout_p,
        is_causal,
        philox_seed,
        philox_offset,
        scale=scale,
    )
    dq, dk, dv = _transpose_dense(dq, dk, dv)
    return dq, dk, dv

