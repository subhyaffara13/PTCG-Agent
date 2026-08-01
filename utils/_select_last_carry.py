
def _select_last_carry(carry_seq: Array, seq_lengths: Array):
  return carry_seq[seq_lengths - 1, jnp.arange(carry_seq.shape[1])]


def _select_last_carry(sequence: A, seq_lengths: jnp.ndarray) -> A:
  last_idx = seq_lengths - 1

  def _slice_array(x: jnp.ndarray):
    return x[last_idx, jnp.arange(x.shape[1])]

  return jax.tree_util.tree_map(_slice_array, sequence)


def _select_last_carry(sequence: A, seq_lengths: jnp.ndarray) -> A:
    last_idx = seq_lengths - 1

    def _slice_array(x: jnp.ndarray):
        return x[last_idx, jnp.arange(x.shape[1])]

    return jax.tree_util.tree_map(_slice_array, sequence)

