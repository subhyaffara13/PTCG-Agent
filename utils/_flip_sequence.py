
def _flip_sequence(sequences: Array, seq_lengths: Array) -> Array:
  max_steps = sequences.shape[0]
  roll_amounts = max_steps - seq_lengths
  # roll initially puts padding at the front so when the sequence is reversed
  # (via [::-1]) the padding stays at the end
  return jax.vmap(partial(jnp.roll, axis=0), in_axes=(1, 0),
      out_axes=1)(sequences, roll_amounts)[::-1]

