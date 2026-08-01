
def _fa3_flash_attention_forward_impl(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    cum_seq_q: torch.Tensor | None,
    cum_seq_k: torch.Tensor | None,
    max_q: int,
    max_k: int,
    dropout_p: float,
    is_causal: bool,
    return_debug_mask: bool,
    q_descale: torch.Tensor | None = None,
    k_descale: torch.Tensor | None = None,
    v_descale: torch.Tensor | None = None,
    *,
    scale: float | None = None,
    window_size_left: int = -1,
    window_size_right: int = -1,
    seqused_k: torch.Tensor | None = None,
    alibi_slopes: torch.Tensor | None = None,
    out: torch.Tensor | None = None,
    block_table: torch.Tensor | None = None,
    compute_auxiliary: bool = True,
    num_splits: int | None = None,
):
    error = _fa3_forward_support_error(
        query,
        key,
        value,
        dropout_p,
        return_debug_mask,
        alibi_slopes,
        seqused_k,
        cum_seq_q,
        q_descale,
        k_descale,
        v_descale,
    )
    if error is not None:
        raise RuntimeError(f"FA3 flash_attention forward unsupported: {error}")
    out, lse = _fa3_run_forward(
        query,
        key,
        value,
        cum_seq_q,
        cum_seq_k,
        max_q,
        max_k,
        scale,
        is_causal,
        window_size_left,
        window_size_right,
        seqused_k,
        out,
        q_descale,
        k_descale,
        v_descale,
        block_table,
        num_splits,
    )
    if compute_auxiliary:
        rng_state = torch.zeros((2,), dtype=torch.uint64, device=query.device)
        philox_offset = torch.zeros((), dtype=torch.uint64, device=query.device)
        debug_mask = torch.empty(0, dtype=query.dtype, device=query.device)
    else:
        rng_state = None
        philox_offset = None
        debug_mask = None
    return out, lse, rng_state, philox_offset, debug_mask

