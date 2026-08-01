
def _sfdp_pattern_18(query, key, value, causal_mask, inv_scale, dropout_p):
    # for hf_GPT2 with dropout (introduces clone node) for inference
    # it also returns permuted key & value
    query = query.permute([0, 2, 1, 3])
    key = key.permute([0, 2, 1, 3])
    value = value.permute([0, 2, 1, 3])
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
    return (
        (
            torch.nn.functional.dropout(attn_weights.softmax(dim=-1), dropout_p).matmul(
                value
            )
        ),
        key,
        value,
    )

