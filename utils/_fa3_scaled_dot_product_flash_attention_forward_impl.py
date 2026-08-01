
def _fa3_scaled_dot_product_flash_attention_forward_impl(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    q_descale: torch.Tensor | None = None,
    k_descale: torch.Tensor | None = None,
    v_descale: torch.Tensor | None = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    return_debug_mask: bool = False,
    *,
    scale: float | None = None,
):
    error = _fa3_forward_support_error(
        query,
        key,
        value,
        dropout_p,
        return_debug_mask,
        None,
        None,
        None,
        q_descale,
        k_descale,
        v_descale,
    )
    if error is not None:
        raise RuntimeError(f"FA3 SDPA forward unsupported: {error}")
    q, k, v = _transpose_dense(query, key, value)

    # Pre-allocate output with query's strides (BHSD layout), then create
    # a BSHD view for the kernel. This ensures the returned output has
    # the same memory layout as the input query.
    out_dtype = torch.bfloat16 if query.dtype == torch.float8_e4m3fn else query.dtype
    out_bhsd = torch.empty_like(query, dtype=out_dtype)
    out_bshd = out_bhsd.transpose(1, 2)

    max_q_flash = q.size(1)
    max_k_flash = k.size(1)
    _, lse, rng_state, philox_offset, debug_mask = _fa3_flash_attention_forward_impl(
        q,
        k,
        v,
        None,
        None,
        max_q_flash,
        max_k_flash,
        dropout_p,
        is_causal,
        return_debug_mask,
        scale=scale,
        out=out_bshd,
        q_descale=q_descale,
        k_descale=k_descale,
        v_descale=v_descale,
    )
    max_q = query.size(2)
    max_k = key.size(2)
    return (
        out_bhsd,
        lse,
        None,
        None,
        max_q,
        max_k,
        rng_state,
        philox_offset,
        debug_mask,
    )

