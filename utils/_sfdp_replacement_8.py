
def _sfdp_replacement_8(query, key, value, inv_scale):
    counters["inductor"]["fuse_attention"] += 1
    q = query.permute(0, 2, 1, 3)
    k = key.permute(0, 2, 1, 3)
    v = value.permute(0, 2, 1, 3)
    return _scaled_dot_product_attention(
        q,
        k,
        v,
        attn_mask=None,  # attn_mask,
        dropout_p=0.0,
        scale=1.0 / inv_scale,
        is_causal=False,
    )

