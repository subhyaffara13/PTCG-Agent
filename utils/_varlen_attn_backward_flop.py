
def _varlen_attn_backward_flop(
    grad_out,
    query,
    key,
    value,
    out,
    lse,
    cu_seq_q,
    cu_seq_k,
    max_q,
    max_k,
    *args,
    out_val=None,
    **kwargs,
) -> int:
    """Count flops for varlen_attn backward."""
    sizes = _unpack_flash_attention_nested_shapes(
        query=query,
        key=key,
        value=value,
        grad_out=grad_out,
        cum_seq_q=cu_seq_q,
        cum_seq_k=cu_seq_k,
        max_q=max_q,
        max_k=max_k,
    )
    return sum(
        sdpa_backward_flop_count(grad_out_shape, query_shape, key_shape, value_shape)
        for query_shape, key_shape, value_shape, grad_out_shape in sizes
    )

