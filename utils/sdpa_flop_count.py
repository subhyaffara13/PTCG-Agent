
def sdpa_flop_count(query_shape, key_shape, value_shape):
    """
    Count flops for self-attention.

    Supports GQA (grouped-query attention) where key/value have fewer heads
    than the query. The kernel broadcasts KV heads to match query heads.
    """
    b, h_q, s_q, d_q = query_shape
    _b2, h_kv, s_k, _d2 = key_shape
    _b3, _h3, _s3, d_v = value_shape
    if not (b == _b2 == _b3 and h_kv == _h3 and d_q == _d2 and s_k == _s3):
        raise AssertionError(
            f"sdpa_flop_count: query/key/value shapes are incompatible: "
            f"q={query_shape}, k={key_shape}, v={value_shape}"
        )
    if h_q < h_kv or h_q % h_kv != 0:
        raise AssertionError(
            f"sdpa_flop_count: query heads ({h_q}) must be a multiple of "
            f"key/value heads ({h_kv})"
        )
    total_flops = 0
    # q: [b, h_q, s_q, d_q] @ k: [b, h_q, d_q, s_k] -> scores: [b, h_q, s_q, s_k]
    total_flops += bmm_flop((b * h_q, s_q, d_q), (b * h_q, d_q, s_k))
    # scores: [b, h_q, s_q, s_k] @ v: [b, h_q, s_k, d_v] -> out: [b, h_q, s_q, d_v]
    total_flops += bmm_flop((b * h_q, s_q, s_k), (b * h_q, s_k, d_v))
    return total_flops

