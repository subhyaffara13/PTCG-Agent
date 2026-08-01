
def _sfdp_pattern_21(query, key, value, attn_mask):
    # for T5 with inplace add
    query = query.permute([0, 2, 1, 3])
    key = key.permute([0, 2, 1, 3])
    value = value.permute([0, 2, 1, 3])
    score = torch.matmul(query, key.permute(0, 1, 3, 2))
    masked_score = score + attn_mask
    score = masked_score.type_as(query)
    return score.float().softmax(dim=-1).type_as(query).matmul(value)

