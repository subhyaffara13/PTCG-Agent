
def _prepare_4d_attention_mask_inverted(mask: torch.Tensor, dtype: torch.dtype, tgt_len: int | None = None):
    """
    Expands attention_mask from `[bsz, seq_len]` to `[bsz, 1, tgt_seq_len, src_seq_len]`.
    """
    bsz, src_len = mask.size()
    tgt_len = tgt_len if tgt_len is not None else src_len

    expanded_mask = mask[:, None, None, :].expand(bsz, 1, tgt_len, src_len).to(dtype)

    inverted_mask = 1.0 - expanded_mask
    expanded_attention_mask = inverted_mask.masked_fill(inverted_mask.bool(), torch.finfo(dtype).min)

    # make sure that global_attn_mask is positive
    expanded_attention_mask = expanded_attention_mask * inverted_mask

    return expanded_attention_mask

