
def _fa3_scaled_dot_product_flash_attention_backward_impl(
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
    """FA3 implementation of _scaled_dot_product_flash_attention_backward."""
    error = _fa3_backward_support_error(
        grad_out, query, key, value, out, logsumexp, dropout_p, None, None, None
    )
    if error is not None:
        raise RuntimeError(f"FA3 SDPA backward unsupported: {error}")

    # SDPA uses BHSD layout, FA3 uses BSHD - transpose
    grad_out_t, q_t, k_t, v_t, out_t = _transpose_dense(
        grad_out, query, key, value, out
    )

    dq, dk, dv = _fa3_flash_attention_backward_impl(
        grad_out_t,
        q_t,
        k_t,
        v_t,
        out_t,
        logsumexp,
        None,  # cum_seq_q (dense attention)
        None,  # cum_seq_k
        max_q,  # max_seqlen_q
        max_k,  # max_seqlen_k
        dropout_p,
        is_causal,
        philox_seed,
        philox_offset,
        scale=scale,
    )

    # Transpose gradients back to BHSD layout
    dq_out, dk_out, dv_out = _transpose_dense(dq, dk, dv)
    return dq_out, dk_out, dv_out

