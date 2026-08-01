
def _sfdp_replacement_28(query, key, value, scale_factor, dropout_p):
    counters["inductor"]["fuse_attention"] += 1
    return _scaled_dot_product_attention(
        query.contiguous(),
        key.contiguous(),
        value.contiguous(),
        attn_mask=None,
        dropout_p=dropout_p,
        is_causal=False,
        scale=scale_factor,
    )

