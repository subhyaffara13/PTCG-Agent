
def _sfdp_pattern_19(query, key, value, causal_mask, attn_mask, inv_scale, dropout_p):
    # for token-classification+gpt2 / text-generation+gpt2
    attn_weights = torch.matmul(query, key.permute(0, 1, 3, 2))
    inv_scale = torch.full(
        [],
        inv_scale,
        dtype=attn_weights.dtype,
        device=attn_weights.device,
    )
    attn_weights = attn_weights.div(inv_scale)
    causal_mask_value = torch.full(
        (), torch.finfo(query.dtype).min, dtype=query.dtype, device=query.device
    )
    attn_weights = torch.where(causal_mask, attn_weights, causal_mask_value)
    attn_weights = attn_weights + attn_mask
    attn_weights = attn_weights.softmax(dim=-1).type(value.dtype)
    return torch.nn.functional.dropout(attn_weights, dropout_p).matmul(value)

