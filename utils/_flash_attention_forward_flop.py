
def _flash_attention_forward_flop(
    query,
    key,
    value,
    cum_seq_q,
    cum_seq_k,
    max_q,
    max_k,
    *args,
    out_shape=None,
    **kwargs
) -> int:
    """Count flops for self-attention."""
    # NB: We aren't accounting for causal attention here
    # in case this is a nested tensor, we unpack the individual batch elements
    # and then sum the flops per batch element
    sizes = _unpack_flash_attention_nested_shapes(
        query=query,
        key=key,
        value=value,
        cum_seq_q=cum_seq_q,
        cum_seq_k=cum_seq_k,
        max_q=max_q,
        max_k=max_k,
    )
    return sum(
        sdpa_flop_count(query_shape, key_shape, value_shape)
        for query_shape, key_shape, value_shape, _ in sizes
    )

