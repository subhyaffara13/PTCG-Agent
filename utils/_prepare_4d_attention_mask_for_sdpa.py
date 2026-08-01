
def _prepare_4d_attention_mask_for_sdpa(mask: torch.Tensor, dtype: torch.dtype, tgt_len: int | None = None):
    """
    Creates a non-causal 4D mask of shape `(batch_size, 1, query_length, key_value_length)` from a 2D mask of shape
    `(batch_size, key_value_length)`

    Args:
        mask (`torch.Tensor`):
            A 2D attention mask of shape `(batch_size, key_value_length)`
        dtype (`torch.dtype`):
            The torch dtype the created mask shall have.
        tgt_len (`int`):
            The target length or query length the created mask shall have.
    """
    warnings.warn(DEPRECATION_MESSAGE, FutureWarning)

    _, key_value_length = mask.shape
    tgt_len = tgt_len if tgt_len is not None else key_value_length

    # torch.jit.trace, symbolic_trace and torchdynamo with fullgraph=True are unable to capture data-dependent controlflows.
    if not is_tracing(mask) and torch.all(mask == 1):
        return None
    else:
        return AttentionMaskConverter._expand_mask(mask=mask, dtype=dtype, tgt_len=tgt_len)

