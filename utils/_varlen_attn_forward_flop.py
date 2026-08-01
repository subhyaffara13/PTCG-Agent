
def _varlen_attn_forward_flop(
    query,
    key,
    value,
    cu_seq_q,
    cu_seq_k,
    max_q,
    max_k,
    *args,
    out_val=None,
    **kwargs,
) -> int:
    """Count flops for varlen_attn forward."""
    sizes = _unpack_flash_attention_nested_shapes(
        query=query,
        key=key,
        value=value,
        cum_seq_q=cu_seq_q,
        cum_seq_k=cu_seq_k if cu_seq_k is not None else cu_seq_q,
        max_q=max_q,
        max_k=max_k,
    )
    return sum(
        sdpa_flop_count(query_shape, key_shape, value_shape)
        for query_shape, key_shape, value_shape, _ in sizes
    )

