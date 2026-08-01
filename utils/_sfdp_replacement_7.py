
def _sfdp_replacement_7(query, key, value, inv_scale, dropout_p):
    # sdpa prefers inputs in permuted format
    # it makes a copy to put them in this format
    # if they aren't already
    # to make replacement efficient ensure that inputs to sdpa
    # are in required order
    counters["inductor"]["fuse_attention"] += 1
    q = query.permute(0, 2, 1, 3)
    k = key.permute(0, 2, 1, 3)
    v = value.permute(0, 2, 1, 3)
    return _scaled_dot_product_attention(
        q,
        k,
        v,
        attn_mask=None,  # attn_mask,
        dropout_p=dropout_p,
        scale=1.0 / inv_scale,
        is_causal=False,
    )

