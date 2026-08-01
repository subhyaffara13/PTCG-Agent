
def _efficient_attention_backward_flop(
    grad_out,
    query,
    key,
    value,
    bias,
    out,  # named _out to avoid kwarg collision with out created in wrapper
    cu_seqlens_q,
    cu_seqlens_k,
    max_seqlen_q,
    max_seqlen_k,
    *args,
    **kwargs,
) -> int:
    # in case this is a nested tensor, we unpack the individual batch elements
    # and then sum the flops per batch element
    shapes = _unpack_efficient_attention_nested_shapes(
        query=query,
        key=key,
        value=value,
        grad_out=grad_out,
        cu_seqlens_q=cu_seqlens_q,
        cu_seqlens_k=cu_seqlens_k,
        max_seqlen_q=max_seqlen_q,
        max_seqlen_k=max_seqlen_k,
    )
    return sum(
        sdpa_backward_flop_count(grad_out_shape, query_shape, key_shape, value_shape)
        for query_shape, key_shape, value_shape, grad_out_shape in shapes
    )

