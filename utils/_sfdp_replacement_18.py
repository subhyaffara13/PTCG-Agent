
def _sfdp_replacement_18(query, key, value, causal_mask, inv_scale, dropout_p):
    counters["inductor"]["fuse_attention"] += 1
    permuted_key = key.transpose(1, 2)
    permuted_value = value.transpose(1, 2)
    return (
        _scaled_dot_product_attention(
            query.transpose(1, 2),
            permuted_key,
            permuted_value,
            attn_mask=causal_mask,
            dropout_p=dropout_p,
            is_causal=False,
            scale=1.0 / inv_scale,
        ),
        permuted_key,
        permuted_value,
    )

