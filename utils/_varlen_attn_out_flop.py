
def _varlen_attn_out_flop(
    out,
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
    """Count flops for varlen_attn_out forward."""
    return _varlen_attn_forward_flop(
        query, key, value, cu_seq_q, cu_seq_k, max_q, max_k,
    )

