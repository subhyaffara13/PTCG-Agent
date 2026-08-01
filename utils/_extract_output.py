
def _extract_output(seq_lengths: Array, out) -> tuple[tuple[Array, Array], Array]:
  _, ((hs, cs), seq_first_y) = out
  h_t = _select_last_carry(hs, seq_lengths)
  c_t = _select_last_carry(cs, seq_lengths)

  # [seq_len, batch]   [1, batch]             [seq_len, 1]
  mask = seq_lengths[None] > jnp.arange(seq_first_y.shape[0], dtype=jnp.int32)[:, None]
  # [batch, seq_len, hidden_size]
  seq_first_y = jnp.where(
      mask[..., None], # [seq_len, batch, 1]
      seq_first_y,     # [seq_len, batch, hidden_size]
      0)
  return (h_t, c_t), seq_first_y

