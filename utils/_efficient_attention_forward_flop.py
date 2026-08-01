
def _efficient_attention_forward_flop(
    query,
    key,
    value,
    bias,
    cu_seqlens_q,
    cu_seqlens_k,
    max_seqlen_q,
    max_seqlen_k,
    *args,
    **kwargs
) -> int:
    """Count flops for self-attention."""
    # NB: We aren't accounting for causal attention here
    # in case this is a nested tensor, we unpack the individual batch elements
    # and then sum the flops per batch element
    sizes = _unpack_efficient_attention_nested_shapes(
        query=query,
        key=key,
        value=value,
        cu_seqlens_q=cu_seqlens_q,
        cu_seqlens_k=cu_seqlens_k,
        max_seqlen_q=max_seqlen_q,
        max_seqlen_k=max_seqlen_k,
    )
    return sum(
        sdpa_flop_count(query_shape, key_shape, value_shape)
        for query_shape, key_shape, value_shape, _ in sizes
    )

