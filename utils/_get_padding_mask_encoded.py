
def _get_padding_mask_encoded(T, q_seqlen):
  q_indices = jnp.arange(0, T)[None, :]
  mask = q_indices < q_seqlen[:, None]
  return mask[:, :, None, None]

