
def _sfdp_replacement_5(query, key, value, attn_mask, inv_scale):
    counters["inductor"]["fuse_attention"] += 1
    return _scaled_dot_product_attention(
        query,
        key,
        value,
        attn_mask=attn_mask.to(dtype=query.dtype),
        dropout_p=0.0,
        scale=1.0 / inv_scale,
        is_causal=False,
    )

