
def _apply_masks(logits, mask, is_causal, q_seqlen, kv_seqlen,
                 local_window_size):
  if mask is None and not is_causal and q_seqlen is None and kv_seqlen is None and local_window_size is None:
    return logits

  combined_mask = jnp.ones_like(logits, dtype=bool)
  if mask is not None:
    assert mask.dtype == np.dtype(bool)
    combined_mask = jnp.logical_and(combined_mask, mask)

  T, S = logits.shape[2], logits.shape[3]

  if is_causal:
    mask = _get_causal_mask(T, S)
    combined_mask = jnp.logical_and(combined_mask, mask)

  if local_window_size is not None:
    mask = _get_window_mask(T, S, local_window_size)
    combined_mask = jnp.logical_and(combined_mask, mask)

  if q_seqlen is not None or kv_seqlen is not None:
    mask = _get_padding_mask_logits(T, S, q_seqlen, kv_seqlen)
    combined_mask = jnp.logical_and(combined_mask, mask)

  large_negative_number = _get_large_negative(logits.dtype)
  padded_logits = jnp.where(combined_mask, logits, large_negative_number)
  return padded_logits

