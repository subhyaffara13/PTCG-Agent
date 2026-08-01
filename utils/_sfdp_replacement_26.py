
def _sfdp_replacement_26(query, key, value, attn_mask, dropout_p):
    counters["inductor"]["fuse_attention"] += 1
    query = query.permute(0, 2, 1, 3)
    key = key.permute(0, 2, 1, 3)
    value = value.permute(0, 2, 1, 3)
    if attn_mask.device.type == "xpu":
        attn_mask = attn_mask.contiguous()
    return (
        _scaled_dot_product_attention(
            query,
            key,
            value,
            attn_mask=attn_mask,
            dropout_p=dropout_p,
            is_causal=False,
            scale=1.0,
        ),
        key,
        value,
    )

