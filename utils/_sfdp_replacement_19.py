
def _sfdp_replacement_19(
    query, key, value, causal_mask, attn_mask, inv_scale, dropout_p
):
    counters["inductor"]["fuse_attention"] += 1
    fill_value = torch.full((), -float("inf"), dtype=query.dtype, device=query.device)
    attn_mask = torch.where(causal_mask, attn_mask, fill_value)
    return _scaled_dot_product_attention(
        query,
        key,
        value,
        attn_mask=attn_mask,
        dropout_p=dropout_p,
        is_causal=False,
        scale=1.0 / inv_scale,
    )

