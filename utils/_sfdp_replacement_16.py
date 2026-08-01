
def _sfdp_replacement_16(query, key, value, attn_mask, inv_scale, dropout_p):
    counters["inductor"]["fuse_attention"] += 1
    return _scaled_dot_product_attention(
        query.transpose(1, 2),
        key.transpose(1, 2),
        value.transpose(1, 2),
        attn_mask=attn_mask.to(dtype=query.dtype),
        dropout_p=dropout_p,
        is_causal=False,
        scale=1.0 / inv_scale,
    )

