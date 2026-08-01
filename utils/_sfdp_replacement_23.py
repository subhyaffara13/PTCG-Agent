
def _sfdp_replacement_23(query, key, value):
    counters["inductor"]["fuse_attention"] += 1
    query = query.permute(0, 2, 1, 3)
    key = key.permute(0, 2, 1, 3)
    value = value.permute(0, 2, 1, 3)
    return (
        _scaled_dot_product_attention(
            query,
            key,
            value,
            attn_mask=None,
            is_causal=False,
            scale=1.0,
        ),
        key,
        value,
    )

