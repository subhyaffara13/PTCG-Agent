
def _sfdp_pattern_16(query, key, value, attn_mask, inv_scale, dropout_p):
    # for BertLarge with dropout
    q = query.permute([0, 2, 1, 3])
    k = key.permute([0, 2, 1, 3])
    v = value.permute([0, 2, 1, 3])
    return (
        torch.nn.functional.dropout(
            (torch.matmul(q, k.transpose(-2, -1)).div(inv_scale) + attn_mask).softmax(
                dim=-1
            ),
            dropout_p,
        )
        .to(dtype=query.dtype)
        .matmul(v)
    )

