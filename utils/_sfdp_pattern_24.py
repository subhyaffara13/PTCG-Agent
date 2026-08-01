
def _sfdp_pattern_24(query, key, value, attention_mask):
    """
    this pattern is for MBartForCausalLM/PLBartForCausalLM.
    attn_mask has a different dtype with QKV.
    there is no scale in sdpa.
    """
    bs = query.size(0)
    n_head = query.size(1)
    seq_len = query.size(2)
    head_size = query.size(3)
    q = query.view(bs * n_head, -1, head_size)
    k = key.reshape(bs * n_head, -1, head_size)
    v = value.reshape(bs * n_head, -1, head_size)
    attn_weights = torch.bmm(q, k.transpose(1, 2))
    attn_weights = attn_weights.view(bs, n_head, seq_len, -1) + attention_mask
    attn_weights = attn_weights.view(bs * n_head, seq_len, -1)
    attn_weights = torch.nn.functional.softmax(attn_weights, dim=-1)
    if query.dtype == torch.half:
        attn_weights = attn_weights.to(torch.half)
    attn_output = torch.bmm(attn_weights, v)
    attn_output = attn_output.view(bs, n_head, seq_len, head_size)
    return attn_output

