
def _flash_attention_backward_flop(
    grad_out,
    query,
    key,
    value,
    out,  # named _out_shape to avoid kwarg collision with out_shape created in wrapper
    logsumexp,
    cum_seq_q,
    cum_seq_k,
    max_q,
    max_k,
    *args,
    **kwargs,
) -> int:
    # in case this is a nested tensor, we unpack the individual batch elements
    # and then sum the flops per batch element
    shapes = _unpack_flash_attention_nested_shapes(
        query=query,
        key=key,
        value=value,
        grad_out=grad_out,
        cum_seq_q=cum_seq_q,
        cum_seq_k=cum_seq_k,
        max_q=max_q,
        max_k=max_k,
    )
    return sum(
        sdpa_backward_flop_count(grad_out_shape, query_shape, key_shape, value_shape)
        for query_shape, key_shape, value_shape, grad_out_shape in shapes
    )

