
def _sfdp_pattern_25(query, key, value, attn_mask, dropout_p):
    # for T5 with inplace add
    query = query.permute([0, 2, 1, 3])
    key = key.permute([0, 2, 1, 3])
    value = value.permute([0, 2, 1, 3])
    score = torch.matmul(query, key.permute(0, 1, 3, 2))
    masked_score = score + attn_mask
    return torch.nn.functional.dropout(
        masked_score.float().softmax(dim=-1).type_as(query), dropout_p
    ).matmul(value)

