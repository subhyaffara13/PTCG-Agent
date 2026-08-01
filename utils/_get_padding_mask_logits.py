
def _get_padding_mask_logits(T, S, q_seqlen, kv_seqlen):
  q_mask = True
  kv_mask = True
  if q_seqlen is not None:
    q_indices = jnp.arange(0, T)[None, :, None]
    q_mask = q_indices < q_seqlen[:, None, None]
  if kv_seqlen is not None:
    kv_indices = jnp.arange(0, S)[None, None, :]
    kv_mask = kv_indices < kv_seqlen[:, None, None]
  mask = jnp.logical_and(q_mask, kv_mask)
  return mask[:, None, :, :]

