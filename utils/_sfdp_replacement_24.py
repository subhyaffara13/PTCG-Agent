
def _sfdp_replacement_24(query, key, value, attention_mask):
    counters["inductor"]["fuse_attention"] += 1
    return _scaled_dot_product_attention(
        query,
        key,
        value,
        attn_mask=attention_mask.to(dtype=query.dtype),
        is_causal=False,
        scale=1,
    )

