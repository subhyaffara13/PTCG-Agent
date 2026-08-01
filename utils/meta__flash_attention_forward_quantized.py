
def meta__flash_attention_forward_quantized(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    cum_seq_q: Tensor | None,
    cum_seq_k: Tensor | None,
    max_q: int,
    max_k: int,
    dropout_p: float,
    is_causal: bool,
    return_debug_mask: bool,
    q_descale: Tensor | None,
    k_descale: Tensor | None,
    v_descale: Tensor | None,
    scale: float | None = None,
    window_size_left: int | None = None,
    window_size_right: int | None = None,
    seqused_k: Tensor | None = None,
    alibi_slopes: Tensor | None = None,
):
    if query.dtype == torch.float8_e4m3fn:
        query = query.to(torch.bfloat16)

    return meta__flash_attention_forward(
        query,
        key,
        value,
        cum_seq_q,
        cum_seq_k,
        max_q,
        max_k,
        dropout_p,
        is_causal,
        return_debug_mask,
        scale,
        window_size_left,
        window_size_right,
        seqused_k,
        alibi_slopes,
    )

